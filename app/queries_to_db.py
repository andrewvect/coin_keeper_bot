import datetime
from .models import db, UserModel, CategoryModel, SubCategoryModel, RegistrationModel, CoinModel
from .service import generate_password, hash_password, get_date_mines_days


def is_user_in_database(user_id, app_context) -> bool:
    with app_context:
        exists = db.session.query(UserModel.user_id).filter_by(user_id=user_id).first() is not None
    return exists


def add_user_to_database(user_id, app_context) -> None:
    with app_context:
        new_user = UserModel(user_id=user_id)
        db.session.add(new_user)
        db.session.commit()


def user_has_category(user_id, category_name, app_context) -> bool:
    with app_context:
        category_exists = db.session.query(CategoryModel).filter_by(name=category_name, user_id=user_id).first()
        return category_exists is not None


def add_category_to_user(user_id, category_name, category_type, app_context) -> None:
    with app_context:
        type_of_coins = None
        if category_type == 'expenses':
            type_of_coins = 1
        elif category_type == 'incomes':
            type_of_coins = 2

        new_category = CategoryModel(name=category_name, user_id=user_id, type_coin=type_of_coins)
        db.session.add(new_category)
        db.session.commit()


def user_has_subcategory(user_id, subcategory_name, app_context) -> bool:
    with app_context:
        category_exists = db.session.query(SubCategoryModel).filter_by(name=subcategory_name, user_id=user_id).first()
        return category_exists is not None


def get_id_and_type_category(user_id, category_name, app_context) -> tuple:
    with app_context:
        id_category = 0
        type_of_coin = 0

        query = db.engine.execute(
            'SELECT id, type_coin FROM "categories" WHERE user_id=%s and name=%s ', (user_id, category_name))

        for row in query:
            id_category += row[0]
            type_of_coin += row[1]

        return id_category, type_of_coin


def add_subcategory_to_user(user_id, message, app_context) -> None:
    message = message.lower().split()
    category_name = message[4]
    subcategory_name = message[2]

    data_for_query = get_id_and_type_category(user_id, category_name, app_context)

    with app_context:
        new = SubCategoryModel(name=subcategory_name, id_category=data_for_query[0], user_id=user_id,
                               type_coin=data_for_query[1])
        db.session.add(new)
        db.session.commit()


def get_all_user_categories_subcategories_by_type(user_id, type_coin, app_context) -> str:
    with app_context:

        get_name_categories = db.engine.execute(
            'SELECT name, id FROM "categories" WHERE user_id={0} and type_coin={1} '.format(user_id,
                                                                                            type_coin))

        get_name_subcategories = db.engine.execute(
            'SELECT name, id_category from "subcategories" where user_id=%s and type_coin=%s', user_id,
            type_coin)

        dictionary_of_categories = []
        dictionary_of_subcategories = []

        for r in get_name_categories:
            dictionary_of_categories.append(dict(r.items()))

        for r in get_name_subcategories:
            dictionary_of_subcategories.append(dict(r.items()))

        list_result = []

        for i in dictionary_of_categories:
            liste = []
            key = i["name"]
            key_id = i["id"]
            liste.append(key)
            for w in dictionary_of_subcategories:
                if w["id_category"] == key_id:
                    liste.append(w["name"])
            list_result.append(liste)

        result = ''

        for i in list_result:
            len_list = len(i)
            result += i[0]
            for w in i[1:len_list]:
                result += '\n' + '  ' + w
            result += '\n'
        return result


def get_all_user_categories_and_subcategories(user_id, app_context) -> str:
    income_categories = get_all_user_categories_subcategories_by_type(user_id, 2, app_context)
    spends_categories = get_all_user_categories_subcategories_by_type(user_id, 1, app_context)
    message_for_user = "Expenses: \n" + spends_categories + "\nIncomes: \n" + income_categories
    return message_for_user


def delete_category(user_id, category_name, app_context) -> None:
    with app_context:
        category = db.session.query(CategoryModel).filter_by(user_id=user_id, name=category_name).first()
        db.session.delete(category)
        db.session.commit()


def delete_subcategory(user_id, subcategory_name, app_context) -> None:
    with app_context:
        category = db.session.query(SubCategoryModel).filter_by(user_id=user_id, name=subcategory_name).first()
        db.session.delete(category)
        db.session.commit()


def rename_category(user_id, category_name, new_category_name, app_context) -> None:
    with app_context:
        db.engine.execute(
            'UPDATE "categories" SET name=%s WHERE user_id=%s and name=%s', (
                new_category_name, user_id, category_name
            ))


def rename_subcategory(user_id, subcategory_name, new_subcategory_name, app_context) -> None:
    with app_context:
        db.engine.execute(
            'UPDATE "subcategories" SET name=%s WHERE user_id=%s and name=%s', (
                new_subcategory_name, user_id, subcategory_name
            ))


def check_if_user_in_registration_base(user_id, app_context) -> bool:
    with app_context:

        exists = db.session.query(RegistrationModel).filter_by(telegram_user=user_id).first() is not None

        if not exists:
            return False
        else:
            return True


def register_user_and_get_details(user_id, username, app_context) -> list:
    with app_context:
        password = generate_password()

        hashered_password = str(hash_password(password))

        new = RegistrationModel(username=username, hash_password=hashered_password, telegram_user=user_id)
        db.session.add(new)
        db.session.commit()
        return [username, password]


def get_id_subcategory(user_id, subcategory_name, app_context) -> int:
    with app_context:
        id_subcategory = ''

        query = db.engine.execute(
            'SELECT id FROM "subcategories" WHERE name=%s AND user_id=%s', (
                subcategory_name, user_id)
        )

        for row in query:
            id_subcategory = row[0]

        return id_subcategory


def add_coin(user_id, value, subcategory_name, app_context) -> None:
    with app_context:
        id_category = get_id_subcategory(user_id, subcategory_name, app_context)

        new_coin = CoinModel(id_subcategory=id_category, value=value,
                             user_id=user_id)
        db.session.add(new_coin)
        db.session.commit()


def check_if_object_category_or_subcategory(object_name, user_id, app_context) -> int:
    if user_has_category(user_id, object_name, app_context) is True:
        return 1
    if user_has_subcategory(user_id, object_name, app_context) is True:
        return 2
    else:
        return 0


def get_coins_by_date_from_category(current_date, start_date, user_id, category_name, app_context) -> int:
    with app_context:
        result = 0

        get_data_by_days = db.engine.execute(f"""SELECT value FROM coins
            JOIN "subcategories" ON coins.id_subcategory=subcategories.id 
            JOIN "categories" ON categories.id=subcategories.id_category WHERE date BETWEEN
            '{start_date}' AND '{current_date}' AND coins.user_id={user_id} AND categories.name='{category_name}';"""
                                             )

        for row in get_data_by_days:
            result += row[0]

        return result


def get_coins_by_date_from_subcategory(current_date, start_date, user_id, subcategory_name, app_context) -> int:
    with app_context:
        result = 0
        get_data_by_days = db.engine.execute(
            f"""SELECT value FROM "coins" JOIN "subcategories" ON coins.id_subcategory=subcategories.id WHERE date BETWEEN
            '{start_date}' AND '{current_date}' AND coins.user_id={user_id} AND "name"='{subcategory_name}'""")

        for row in get_data_by_days:
            result += row[0]

        return result


def get_sum_all_coins_by_date(current_date, start_date, user_id, app_context) -> int:
    with app_context:
        result = 0
        get_data_by_days = db.engine.execute(
            f"""SELECT value FROM "coins" WHERE date BETWEEN
            '{start_date}' AND '{current_date}' AND user_id={user_id}""")

        for row in get_data_by_days:
            result += row[0]

        return result


def get_sum_coins_by_date(message, app_context):
    split_string = message.text.lower().split()
    current_date = datetime.date.today()
    start_date = get_date_mines_days(int(split_string[3]))
    user_id = message.chat.id

    try:
        object_name = split_string[6]
    except IndexError:
        object_name = None

    if object_name is None:
        data = get_sum_all_coins_by_date(current_date, start_date, user_id, app_context)
        return data

    object_type = check_if_object_category_or_subcategory(object_name, user_id, app_context)

    if object_type == 1:
        data = get_coins_by_date_from_category(current_date, start_date, user_id, object_name, app_context)
        return data
    if object_type == 2:
        data = get_coins_by_date_from_subcategory(current_date, start_date, user_id, object_name, app_context)
        return data
    if object_type == 0:
        return "You don't have this category or subcategory"


def get_names_subcategories_by_name_category(category_name, user_id, app_context) -> list:
    result = []
    with app_context:
        a = f"""
            SELECT subcategories.name FROM subcategories 
            JOIN categories ON subcategories.id_category = categories.id
            WHERE subcategories.user_id= {user_id} AND categories.name = '{category_name}'"""

        query = db.engine.execute(
            f"""
            SELECT subcategories.name FROM subcategories 
            JOIN categories ON subcategories.id_category = categories.id
            WHERE subcategories.user_id= {user_id} AND categories.name = '{category_name}'""")
        for row in query:
            result.append(row[0])

    return result


def query_to_get_data_by_category_per_subcategories(user_id, category_name, current_date, start_date, app_context):
    subcategories_names = get_names_subcategories_by_name_category(category_name, user_id, app_context)

    result = {}
    with app_context:

        for i in subcategories_names:
            query = db.engine.execute(
                f"""
            SELECT sum(coins.value) FROM coins 
            JOIN subcategories ON coins.id_subcategory = subcategories.id
            WHERE subcategories.name = '{i}' AND coins.date BETWEEN '{start_date}' AND '{current_date}'""", (
                    category_name, user_id)
            )
            for row in query:
                if row[0] is None:
                    result[i] = row[0]
                else:
                    result[i] = row[0]

    return result


def get_data_for_pipe_chart(message, app_context):
    # draw pipe in category_name for 7 days

    split_string = message.text.lower().split()
    current_date = datetime.date.today()
    start_date = get_date_mines_days(int(split_string[5]))
    category_name = split_string[3]
    user_id = message.chat.id

    if user_has_category(user_id, category_name, app_context) is True:
        return query_to_get_data_by_category_per_subcategories(user_id, category_name, current_date, start_date,
                                                               app_context)


class ApiQueries:
    @staticmethod
    def get_data_from_query(data):
        result = []
        for i in data:
            result.append(i[0])
            result.append(i[1])
        return result

    @staticmethod
    def count_period_days(period):
        time_values = {30: ['month'], 7: ['week'],
                       1: ['day']}
        if period[1] in time_values.values():
            return time_values[period[1]] * period[0]

    def get_user_sum_coins_per_id_subcategory(self, user_id, app_context, period='all'):
        '''

        :param user_id:
        :return dictinary example {1 : 1200, 2 : 300}:
        '''

        with app_context:

            get_user_id_subcategories = db.engine.execute('SELECT id FROM "subcategories" WHERE user_id=%s', (user_id))
            all_coins_per_subcategory = {}
            coins_in_period_per_subcategory = {}

            if period == 'all':

                for row in get_user_id_subcategories:
                    id_subcategory = row[0]
                    coins = (db.engine.execute('SELECT id, value FROM "coins" WHERE user_id=%s and id_subcategory=%s',
                                               (user_id, id_subcategory)))
                    sum_values = 0
                    for value in coins:
                        sum_values += int(value[1])
                    all_coins_per_subcategory[id_subcategory] = sum_values

                return all_coins_per_subcategory

            else:
                date_periods = self.date_periods(period, user_id)
                for row in get_user_id_subcategories:
                    id_subcategory = row[0]
                    for date_period in date_periods:
                        coins = (db.engine.execute(
                            'SELECT id, value FROM "coins" WHERE user_id=%s and id_subcategory=%s and date BETWEEN %s AND %s',
                            (user_id, id_subcategory, date_period[0], date_periods[1])))
                        sum_values = 0
                        for value in coins:
                            sum_values += int(value[1])
                        coins_in_period_per_subcategory[id_subcategory] = [date_period[0], date_period[1], sum_values]

        return all_coins_per_subcategory

    def get_user_sum_coins_per_name_subcategory(self, user_id):
        """
        :param user_id:
        :return dictinary example {'продукты': 28471, 'общественный-транспорт': 1085}:
        """

        get_user_subcategories_name = db.engine.execute('SELECT id, name FROM "subcategories" WHERE user_id=%s',
                                                        (user_id))
        get_sum_coins = self.get_user_sum_coins_per_id_subcategory(user_id)

        subcategory_name_per_sum_coins = {}

        for row in get_user_subcategories_name:
            for id_subcategory, sum_coins in get_sum_coins.items():
                if row[0] == id_subcategory:
                    subcategory_name_per_sum_coins[row[1]] = sum_coins

        return subcategory_name_per_sum_coins

    @staticmethod
    def get_all_user_coins_per_category(user_id, app_context):

        with app_context:
            get_user_categories = db.engine.execute('SELECT id, name FROM "categories" WHERE user_id=%s', user_id)
            get_user_subcategories = db.engine.execute('SELECT id, name FROM "subcategories" WHERE user_id=%s',
                                                       user_id)
            coins_per_subcategory = {}

            for id_subcategory in get_user_subcategories[1]:
                coins = (db.engine.execute('SELECT id, value FROM "coins" WHERE user_id=%s and id_subcategory=%s',
                                           (user_id, id_subcategory)))
                sum_values = sum(coins[1])
                coins_per_subcategory[coins[0]] = sum_values

    @staticmethod
    def count_all_coins_per_subcategorie(user_id, app_context):
        with app_context:
            get_result = (db.engine.execute(
                'DROP VIEW myview; CREATE VIEW myview AS SELECT coins.id_subcategory AS id_subcategory, coins.value, '
                'coins.date, subcategories.name FROM "coins" JOIN "subcategories" ON coins.id_'
                'subcategory=subcategories.id WHERE coins.user_id=%s; SELECT SUM(myview.value), myview.name'
                ' FROM myview GROUP BY myview.name;',
                (user_id)))
            result = {}
            for rows in get_result:
                result[rows[0]] = rows[1]

        return result

    @staticmethod
    def count_sum_coins_per_period_per_all_subcategories(user_id, period, app_context):

        with app_context:
            get_result = (db.engine.execute(
                r"""CREATE OR REPLACE VIEW myview AS SELECT coins.id_subcategory AS id_subcategory, coins.value, 
                coins.date, subcategories.name FROM "coins" JOIN "subcategories" ON coins.id_subcategory=subcategories.id 
                WHERE coins.user_id={0}; 
                SELECT date_trunc('{1}', date ) as start_of_week, sum(value) 
                FROM myview GROUP BY date_trunc('{1}', date ) ORDER BY date_trunc('{1}', date )"""
                    .format(user_id, period)))

            result = {}

            for rows in get_result:
                result[str(rows[0])] = rows[1]

        return result

    @staticmethod
    def count_sum_coins_per_period_per_subcategory(user_id, subcategory_name, period, start_date,
                                                   finish_date, app_context):

        with app_context:
            get_data = (db.engine.execute(
                r"""DROP TABLE IF EXISTS "result";
                CREATE OR REPLACE VIEW myview AS SELECT coins.id_subcategory 
                AS id_subcategory, coins.value, coins.date, subcategories.name 
                FROM "coins" JOIN "subcategories" ON coins.id_subcategory=subcategories.id 
                WHERE coins.user_id={0} AND subcategories.name='{1}' 
                AND coins.date BETWEEN '{3}' AND '{4}'; 
                
                SELECT * FROM myview;
                CREATE TABLE "result" (id int, value int default 0, uploade_date date);
                INSERT INTO "result"(value, uploade_date) SELECT value, date FROM myview;
                CREATE OR REPLACE VIEW date_salt AS SELECT date_trunc('{2}', dd):: date
                FROM generate_series
                ( '{3}'::timestamp , '{4}' ::timestamp, '1 {2}'::interval) dd;
                INSERT INTO "result"( uploade_date) SELECT date_trunc FROM date_salt;
                SELECT date_trunc('{2}', uploade_date ) as start_of_week, sum(value) 
                FROM "result" GROUP BY date_trunc('{2}', uploade_date ) 
                ORDER BY date_trunc('{2}', uploade_date )"""
                    .format(user_id, subcategory_name, period, start_date, finish_date)))

            result = {}

            for rows in get_data:
                result[str(rows[0])] = rows[1]

        return result

    @staticmethod
    def get_user_subcategories(user_id, app_context):
        with app_context:
            get_data = (db.engine.execute('SELECT name from "subcategories" where user_id=%s', user_id))
            result = []
            for row in get_data:
                result.append(row[0])
        return result

    def count_sum_coins_per_period_per_category(self, user_id, category_name, period, start_date, finish_date,
                                                app_context):
        if category_name == "Все траты":
            return self.count_all(user_id, period, app_context)
        else:
            with app_context:
                get_data = db.engine.execute(r"""DROP VIEW IF EXISTS user_categories3;
                    DROP VIEW IF EXISTS user_categories2;
                    DROP TABLE IF EXISTS "result";
    
                    CREATE OR REPLACE VIEW user_categories2 AS SELECT categories.id as id_category,
                    categories.name as categories_name, subcategories.name as subcategories_name, 
                    subcategories.id as id_subcategory
    
                    FROM "categories" JOIN "subcategories" ON categories.id=subcategories.id_category
                    WHERE categories.name='{1}' AND categories.user_id={0};
    
                    CREATE OR REPLACE VIEW user_categories3 AS SELECT coins.value,
                    user_categories2.id_category, user_categories2.categories_name, coins.date  
                    FROM "coins" JOIN user_categories2 ON coins.id_subcategory=user_categories2.id_subcategory
                    WHERE coins.date BETWEEN '{3}' AND '{4}';
    
                    CREATE TABLE "result" (id int, value int default 0, uploade_date date);
                    INSERT INTO "result"(value, uploade_date) SELECT value, date FROM user_categories3;
                    CREATE OR REPLACE VIEW date_salt AS SELECT date_trunc('{2}', dd):: date FROM generate_series
                    ( '{3}'::timestamp , '{4}' ::timestamp, '1 {2}'::interval) dd;
                    INSERT INTO "result"( uploade_date) SELECT date_trunc FROM date_salt;
    
                    SELECT date_trunc('{2}', uploade_date ) as start_of_week, sum(value) 
                    FROM "result" GROUP BY date_trunc('{2}', uploade_date ) 
                    ORDER BY date_trunc('{2}', uploade_date );"""
                                             .format(user_id, category_name, period, start_date, finish_date))

            result = {}

            for rows in get_data:
                result[str(rows[0])] = rows[1]
            return result

    @staticmethod
    def user_categories(user_id, app_context):
        with app_context:
            get_all_categories = db.engine.execute(
                'SELECT name FROM "categories" WHERE user_id=%s', user_id)

        categories_names = []
        for row in get_all_categories:
            categories_names.append(row[0])

        return categories_names

    @staticmethod
    def get_user_income_categories(user_id, type, app_context):
        with app_context:
            get_all_categories = db.engine.execute(
                'SELECT name FROM "categories" WHERE user_id=%s AND type_coin=%s', user_id, type)

        categories_names = []
        for row in get_all_categories:
            categories_names.append(row[0])

        return categories_names

    @staticmethod
    def get_user_income_subcategories(user_id, type, app_context):
        with app_context:
            get_all_categories = db.engine.execute(
                'SELECT name FROM "subcategories" WHERE user_id=%s AND type_coin=%s', user_id, type)

        subcategories_names = []
        for row in get_all_categories:
            subcategories_names.append(row[0])

        return subcategories_names

    @staticmethod
    def count_all(user_id, period, app_context):
        with app_context:
            get_data = db.engine.execute(
                r"""DROP TABLE IF EXISTS "result";
                CREATE OR REPLACE VIEW user_sum_coins AS SELECT value, date FROM "coins" WHERE user_id={0};
                CREATE TABLE "result" (id int, value int default 0, uploade_date date);
                INSERT INTO "result"(value, uploade_date) SELECT value, date FROM user_sum_coins;
                CREATE OR REPLACE VIEW date_salt AS SELECT date_trunc('{1}', dd):: date FROM generate_series
                ( '2022-04-07'::timestamp , now() ::timestamp, '1 {1}'::interval) dd;
                INSERT INTO "result"( uploade_date) SELECT date_trunc FROM date_salt;

                SELECT date_trunc('{1}', uploade_date ) as start_of_week, sum(value) 
                FROM "result" GROUP BY date_trunc('{1}', uploade_date ) 
                ORDER BY date_trunc('{1}', uploade_date );"""
                    .format(user_id, period))

        result = {}

        for rows in get_data:
            result[str(rows[0])] = rows[1]
        return result

    @staticmethod
    def get_user_date_registration(user_id, app_context):
        with app_context:
            get_all_categories = db.engine.execute(
                'SELECT created_at FROM "user" WHERE user_id=%s ', user_id)

        date = []
        for row in get_all_categories:
            date.append(row[0])

        return date

    @staticmethod
    def get_all_coins(user_id, period, start_date, finish_date, type_coin, app_context):
        with app_context:
            get_result = db.engine.execute(
                r"""CREATE OR REPLACE VIEW myview 
                AS SELECT coins.id_subcategory AS id_subcategory, coins.value, coins.date, subcategories.name 
                FROM "coins" JOIN "subcategories" ON coins.id_subcategory=subcategories.id 
                WHERE coins.user_id={0} AND subcategories.type_coin={4} AND coins.date BETWEEN '{2}' AND '{3}' ;
                WITH weeks AS (SELECT generate_series('{2}'::date, '{3}'::date, '1 {1}'::interval) 
                AS week_start) 
                SELECT date_trunc('{1}', w.week_start) as start_of_week, COALESCE(sum(m.value), 0) as total_value
                FROM weeks w
                LEFT JOIN myview m ON date_trunc('{1}', m.date) = w.week_start
                GROUP BY start_of_week
                ORDER BY start_of_week;"""
                    .format(user_id, period, start_date, finish_date, type_coin))

            result = {}

            for rows in get_result:
                result[str(rows[0])] = rows[1]

        return result
