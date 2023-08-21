import time
from functools import wraps
import telebot
from flask import Blueprint, jsonify, request, current_app

from .draw_statistic import draw_pipe_diagram
from .logger import logger
from .extantions import bot
from .service import  is_add_category_command, is_add_subcategory_command, \
    is_show_categories_command, is_delete_category_command, \
    is_delete_subcategory_command, is_rename_category_command, is_rename_subcategory_command, \
    get_help_message, is_add_coin_command, is_show_statistic_command, is_draw_pipe_command, add_random_coin_sticker

from .queries_to_db import is_user_in_database, add_user_to_database, user_has_category, \
    add_category_to_user, user_has_subcategory, add_subcategory_to_user, get_all_user_categories_and_subcategories, \
    delete_category, delete_subcategory, rename_subcategory, rename_category, \
    add_coin, get_sum_coins_by_date, get_data_for_pipe_chart

telegram_webhook = Blueprint('webhook', __name__, url_prefix='/webhook')
tg_context = None


@telegram_webhook.route('/', methods=['GET', 'POST'])
def webhook():
    # Function use as webhook handler
    resp = jsonify(success=True)
    if request.method == 'GET':
        return '<h1>Webhook is working<h1>'

    if request.method == 'POST':
        try:
            r = request.get_json()
            global tg_context
            tg_context = current_app.app_context()
            update = telebot.types.Update.de_json(r)
            bot.process_new_updates([update])
            return resp

        except Exception as exc:
            logger.exception('An error occurred: %s', str(exc))
            return resp


def user_exists(func):
    @wraps(func)
    def wrapper(message):

        if is_user_in_database(message.chat.id, tg_context):
            return func(message)
        if not user_exists:
            bot.reply_to(message, "You are not in database.")

    return wrapper


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.reply_to(message, get_help_message())


@bot.message_handler(commands=['start'])
def add_user(message):
    try:
        if is_user_in_database(message.chat.id, tg_context):
            bot.reply_to(message, "You already in database")
            return
        else:
            add_user_to_database(message.chat.id, tg_context)
            bot.reply_to(message, "Welcome to Coin bot!")
            bot.reply_to(message, "You added")

    except Exception as exc:
        logger.exception('An error occurred: %s', str(exc))
        bot.reply_to(message, "Failed to handle command")


@bot.message_handler(func=is_add_category_command)
@user_exists
def handle_add_category(message):
    """Add category to user"""
    try:

        category_name = message.text.split()[2]
        category_type = message.text.split()[4]

        if user_has_category(message.chat.id, category_name, tg_context):
            bot.reply_to(message, "Category already exists")
            return
        else:
            add_category_to_user(message.chat.id, category_name, category_type, tg_context)
            bot.reply_to(message, "Category is added ☺")

    except Exception as exc:
        logger.exception('An error occurred: %s', str(exc))
        bot.reply_to(message, "Failed to add new category")


@bot.message_handler(func=is_add_subcategory_command)
@user_exists
def handle_add_subcategory(message):
    try:
        category_name = message.text.lower().split()[4]

        if user_has_category(message.chat.id, category_name, tg_context) is False:
            bot.reply_to(message, "You don't have this category")
            return

        if user_has_subcategory(message.chat.id, message.text, tg_context):
            bot.reply_to(message, "Subcategory already exists")
            return

        else:
            add_subcategory_to_user(message.chat.id, message.text, tg_context)
            bot.reply_to(message, "Subcategory is added ☺")

    except Exception as exc:
        logger.exception('An error occurred: %s', str(exc))
        bot.reply_to(message, "Failed to add new subcategory")


@bot.message_handler(func=is_show_categories_command)
@user_exists
def handle_show_categories(message):
    try:
        result = get_all_user_categories_and_subcategories(message.chat.id, tg_context)
        bot.reply_to(message, result)

    except Exception as exc:
        logger.exception('An error occurred: %s', str(exc))
        bot.reply_to(message, "Failed to handle command")


@bot.message_handler(func=is_delete_category_command)
@user_exists
def handle_delete_category(message):
    try:

        if user_has_category(message.chat.id, message.text.split()[2], tg_context) is False:
            bot.reply_to(message, "You don't have this category")
            return

        else:
            delete_category(message.chat.id, message.text.split()[2], tg_context)
            bot.reply_to(message, "Deleted category")

    except Exception as exc:
        logger.exception('An error occurred: %s', str(exc))
        bot.reply_to(message, "Failed to handle delete command")


@bot.message_handler(func=is_delete_subcategory_command)
@user_exists
def handle_delete_subcategory(message):
    try:

        if user_has_subcategory(message.chat.id, message.text.split()[2], tg_context) is False:
            bot.reply_to(message, "You don't have this subcategory")
            return
        else:
            delete_subcategory(message.chat.id, message.text.split()[2], tg_context)
            bot.reply_to(message, "Deleted subcategory")

    except Exception as exc:
        logger.exception('An error occurred: %s', str(exc))
        bot.reply_to(message, "Failed to handle delete command")


@bot.message_handler(func=is_rename_category_command)
@user_exists
def handle_rename_category(message):
    try:
        if user_has_category(message.chat.id, message.text.split()[2], tg_context) is False:
            bot.reply_to(message, "You don't have this category")
            return
        else:
            rename_category(message.chat.id, message.text.split()[2], message.text.split()[4], tg_context)
            bot.reply_to(message, "Success")

    except Exception as exc:
        logger.exception('An error occurred: %s', str(exc))
        bot.reply_to(message, "Failed to handle rename command")


@bot.message_handler(func=is_rename_subcategory_command)
@user_exists
def handle_rename_subcategory(message):
    try:
        if user_has_subcategory(message.chat.id, message.text.split()[2], tg_context) is False:
            bot.reply_to(message, "You don't have this subcategory")
            return
        else:
            rename_subcategory(message.chat.id, message.text.split()[2], message.text.split()[4], tg_context)
            bot.reply_to(message, "Success")

    except Exception as exc:
        logger.exception('An error occurred: %s', str(exc))
        bot.reply_to(message, "Failed to handle rename command")


@bot.message_handler(func=is_add_coin_command)
@user_exists
def handle_add_coin(message):
    try:

        if user_has_subcategory(message.chat.id, message.text.split()[2], tg_context) is False:
            bot.reply_to(message, "You don't have this subcategory")
            return
        else:
            add_coin(message.chat.id, message.text.split()[0], message.text.split()[2], tg_context)
            bot.reply_to(message, "Success added value")
            sticker_message = bot.send_sticker(message.chat.id, add_random_coin_sticker())
            time.sleep(2)
            bot.delete_message(chat_id=sticker_message.chat.id, message_id=sticker_message.message_id)

    except Exception as exc:
        logger.exception('An error occurred: %s', str(exc))
        bot.reply_to(message, "Failed to handle registration command")


@bot.message_handler(func=is_show_statistic_command)
@user_exists
def handle_show_statistic(message):
    try:
        result = get_sum_coins_by_date(message, tg_context)
        bot.reply_to(message, result)

    except Exception as exc:
        logger.exception('An error occurred: %s', str(exc))
        bot.reply_to(message, "Failed to handle show statistic command")


@bot.message_handler(func=is_draw_pipe_command)
@user_exists
def handle_draw_pipe_chart(message):
    try:
        if user_has_category(message.chat.id, message.text.split()[3], tg_context) is True:
            data = get_data_for_pipe_chart(message, tg_context)
            pipe_chart = draw_pipe_diagram(data)
            with open(pipe_chart, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        else:
            bot.reply_to(message, "You don't have this category")

    except Exception as exc:
        logger.exception('An error occurred: %s', str(exc))
        bot.reply_to(message, "Failed to handle draw statistic")


@bot.message_handler(func=lambda message: True)
def handle_invalid_commands(message):
    bot.reply_to(message, "Invalid command 😔")
