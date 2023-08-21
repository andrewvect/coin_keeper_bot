import datetime

from flask import Blueprint

from .extantions import scheduler, bot
from .service import get_date_mines_days
from .models import db, engine
from .draw_statistic import draw_pipe_diagram

schedule_blue_print = Blueprint('schedule', __name__, url_prefix='/schedule')


def date_ranges(period):
    count_days = 0
    if period == "week":
        count_days += 60
    if period == "month":
        count_days += 90

    current_date = str(datetime.date.today())
    start_date = get_date_mines_days(count_days)

    previous_period_current_date = get_date_mines_days(count_days + 1)
    previous_period_start_date = get_date_mines_days(count_days * 2)
    return {"current_date": current_date, "start_date": start_date,
            "previous_period_start_date": previous_period_start_date,
            "previous_period_current_date": previous_period_current_date}


def get_stats_spends_by_range_date_by_subcategories(user_id, period):
    date_range = date_ranges(period)

    def get_data(start_date, current_date, user_id):
        with engine.connect() as con:
            data = con.engine.execute(r"""drop view if exists myview5;
                                         CREATE OR REPLACE VIEW myview5 AS
                                         SELECT coins.value, subcategories.name, coins.user_id FROM "coins" JOIN 
                                         "subcategories" ON
                                         coins.id_subcategory=subcategories.id
                                         WHERE coins.date BETWEEN %s and %s and coins.user_id=%s;
                                         SELECT name, SUM(value)
                                         FROM myview1
                                         GROUP BY name;""", (start_date, current_date, user_id))
            return data

    def get_data_with_categories(start_date, current_date, user_id):
        with scheduler.app.app_context():
            data = db.engine.execute(r"""drop view if exists myview3;
                                         drop view if exists myview2;
                                         drop view if exists myview1;
                                         drop view if exists categories_view;

                                         CREATE OR REPLACE VIEW categories_view AS
                                         SELECT categories.name as category_name, categories.id as category_id, 
                                         categories.user_id, subcategories.name, subcategories.id FROM "categories" 
                                         JOIN "subcategories"
                                         ON categories.id=subcategories.id_category;

                                         CREATE OR REPLACE VIEW myview1 AS
                                         SELECT coins.value, subcategories.id_category as id_category, 
                                         subcategories.name, coins.user_id FROM "coins" JOIN "subcategories" ON
                                         coins.id_subcategory=subcategories.id
                                         WHERE coins.date BETWEEN %s and %s and coins.user_id=%s ;

                                         CREATE OR REPLACE VIEW myview2 AS
                                         SELECT id_category, name, SUM(value) FROM myview1
                                         GROUP BY name, id_category;

                                         CREATE OR REPLACE VIEW myview3 AS
                                         SELECT myview2.sum, categories_view.category_name FROM myview2 JOIN 
                                         categories_view ON myview2.id_category=categories_view.category_id;

                                         SELECT SUM(sum), category_name FROM myview3 GROUP BY category_name;""",
                                     (start_date, current_date, user_id))
            return data

    categories_names = []
    categories_values = []
    subcategories_names = []
    values = []
    total_spend = 0
    previous_total_spend = 0

    for row in get_data_with_categories(date_range["start_date"], date_range["current_date"], user_id):
        categories_names.append(row[1])
        categories_values.append(row[0])

    for row in get_data(date_range["start_date"], date_range["current_date"], user_id):
        subcategories_names.append(row[0])
        values.append(row[1])
        total_spend += int(row[1])

    for row in get_data(date_range["previous_period_start_date"], date_range["previous_period_current_date"], user_id):
        previous_total_spend += int(row[1])

    return {"subcategories_names": subcategories_names, "values": values, "total_spend": total_spend,
            "previous_total_spend": previous_total_spend, "period": period, "categories_names": categories_names,
            "categories_values": categories_values}


def get_all_users_id_from_db():
    with engine.connect() as con:
        get_data = con.engine.execute('SELECT user_id FROM "user"')
        users_id = []
        for row in get_data:
            users_id.append(row[0])
        return users_id


def user_spends_by_date_range(user_id, period):
    if period == 'week':
        return get_stats_spends_by_range_date_by_subcategories(user_id, 'week')

    if period == "month":
        return get_stats_spends_by_range_date_by_subcategories(user_id, 'month')


def create_message_with_spends(user_data):
    data_subcategories = ""
    data_categories = ""
    for subcategory, value in zip(user_data['subcategories_names'], user_data['values']):
        data_subcategories += "  " + subcategory + ': ' + str(value) + "\n"

    for subcategory, value in zip(user_data['categories_names'], user_data['categories_values']):
        data_categories += "  " + subcategory + ': ' + str(value) + "\n"

    previous_different = int(user_data["total_spend"]) - int(user_data["previous_total_spend"])
    if previous_different > 0:
        previous_different = "Больше на " + str(previous_different) + " чем "
    if previous_different < 0:
        previous_different = "Меньше на " + str(previous_different)[1:] + " чем "
    if previous_different == 0:
        previous_different = "Такие же траты как и на прошлой"

    article = ""
    path_of_message = ""
    path_of_message2 = ""
    if user_data["period"] == "month":
        article += "=Ежемесячный отчет="
        path_of_message += "в прошлом месяце"
        path_of_message2 += "месяц"

    if user_data["period"] == "week":
        article += "=Еженедельный отчет="
        path_of_message += "на прошлой недели"
        path_of_message2 += "неделю"

    count_percents = abs(round(int(user_data["previous_total_spend"]) / (user_data["total_spend"] * 0.01)))

    text_message = "{4}" \
                   "\n\nТраты за {6} составили: {0}" \
                   "\n\n{2}{5}" \
                   " или на {3}% " \
                   "\n\nТраты по подкатегориям:\n" \
                   "{1}" \
                   "\nТраты по категориям:\n" \
                   "{7}\n\n".format(user_data["total_spend"], data_subcategories, previous_different, count_percents, article,
                                path_of_message, path_of_message2, data_categories)

    return text_message


def send_message_with_spends_by_subcategories_per_period(period):
    users_id_from_db = get_all_users_id_from_db()
    for i in users_id_from_db:
        user_data = user_spends_by_date_range(i, period)
        message = create_message_with_spends(user_data)

        jpg_pipe_chart = draw_pipe_diagram(
            {user_data["subcategories_names"][item]: user_data["values"][item] for item in range(len(user_data["values"]))})
        img = open(jpg_pipe_chart, 'rb')
        bot.send_photo(i, img)

        jpg_pipe_chart2 = draw_pipe_diagram(
            {user_data["categories_names"][item]: user_data["categories_values"][item] for item in
             range(len(user_data["categories_values"]))})
        img2 = open(jpg_pipe_chart2, 'rb')
        bot.send_photo(i, img2)

        bot.send_message(i, message)

#
# @scheduler.scheduled_job('cron', id='week_spend', week='*', day_of_week='mon')
# def week_spend():
#     send_message_with_spends_by_subcategories_per_period('week')
#
#
# @scheduler.scheduled_job('cron', id='month_spend', month='*', day=1)
# def month_spend():
#     send_message_with_spends_by_subcategories_per_period('month')


# @scheduler.task("interval", id="do_job_1", seconds=5)
# def test_task():
#     send_message_with_spends_by_subcategories_per_period('week')

