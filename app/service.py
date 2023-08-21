import datetime
import random
import string

import bcrypt


def get_last_month_date():
    today = datetime.date.today()
    last_month = today - datetime.timedelta(weeks=4.3)
    return last_month.strftime("%Y-%m-%d")


def get_date_mines_days(days):
    today = datetime.date.today()
    result = today - datetime.timedelta(days=days)
    return result.strftime("%Y-%m-%d")


def get_list_of_date(days):
    today = datetime.date.today()
    today_date = today.strftime("%Y-%m-%d")
    list_dt = []
    list_dt.append(today_date)
    for i in range(days):
        a = (today - datetime.timedelta(days=1))
        list_dt.append(a.strftime("%Y-%m-%d"))
        today = a
    return list_dt


def get_tags_from_message(message_list):
    tags = []
    count = 0
    message = " ".join(message_list[3:])
    if len(message) > 0:
        for i in message:
            if i == '(' or i == ')':
                count += 1

        open_bracket_index = message.index('(')
        close_bracket_index = message.index(')')

        if open_bracket_index < close_bracket_index and count == 2:
            str_tags = message[open_bracket_index + 1:close_bracket_index]
            str_tags = str_tags.translate(str.maketrans('', '', '!@#$,'))
            print(str_tags)
            for i in str_tags.split(' '):
                if i != '':
                    tags.append(i)

    return tags



def add_random_coin_sticker():
    sicker_urls = ['CAACAgIAAxkBAAPAYmArRNmhWqFPWFcbCgZxEjz190YAAq8KAAI8HplK2o9PwXKyVAABJAQ',
                   'CAACAgIAAxkBAAO_YmArQLGr8EZsie8rIK2uhejnBzMAAq8MAAJYBEBKm3XVO0aqYvwkBA',
                   'CAACAgIAAxkBAAO-YmArPQ_yLw3UgfM6DYCuZczar0EAAocMAALy2ihLJHffmTImWeEkBA',
                   'CAACAgIAAxkBAAO9YmArLuyFHsUY0gzkRZm0FJ80F2gAAn0MAALKD0BKT-UckWN6lWokBA']

    return random.choice(sicker_urls)


def generate_password():
    allowed_chars = string.ascii_letters + string.digits
    password = ''.join(random.choice(allowed_chars) for _ in range(8))
    return password


def hash_password(password):
    bytePwd = password.encode('utf-8')
    mySalt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytePwd, mySalt)
    return hash


def check_hash_password(password, user_hash_password):
    password_for_check = password.encode('utf-8')
    result = bcrypt.checkpw(password_for_check, bytes(user_hash_password[2:-1], 'utf-8'))

    return result


def is_add_to_database_command(message):
    return message.text == "addtodatabase"


def is_add_category_command(message) -> bool:
    split_str = message.text.lower().split()
    if len(split_str) == 5 \
            and split_str[0] == 'add' \
            and split_str[1] == 'category' \
            and split_str[2].isalpha() \
            and split_str[3] == 'as' \
            and (split_str[4] == 'incomes' or split_str[4] == 'expenses'):
        return True
    else:
        return False


def is_add_subcategory_command(message) -> bool:
    split_string = message.text.lower().split()
    if len(split_string) == 5 \
            and split_string[0] == 'add' \
            and split_string[1] == 'subcategory' \
            and split_string[3] == 'in':
        return True
    return False


def is_show_categories_command(message) -> bool:
    split_string = message.text.lower().split()
    if len(split_string) == 2:
        if split_string[0] == 'show' and split_string[1] == 'categories' or split_string[1] == 'subcategories':
            return True
    return False


def is_delete_category_command(message) -> bool:
    split_string = message.text.lower().split()
    if len(split_string) == 3:
        if split_string[0] == 'delete' and split_string[1] == 'category':
            return True
    return False


def is_delete_subcategory_command(message) -> bool:
    split_string = message.text.lower().split()
    if len(split_string) == 3:
        if split_string[0] == 'delete' and split_string[1] == 'subcategory':
            return True
    return False


def is_rename_category_command(message) -> bool:
    split_string = message.text.lower().split()
    if len(split_string) == 5:
        if split_string[0] == 'rename' and split_string[1] == 'category' and split_string[3] == 'to':
            return True
    return False


def is_rename_subcategory_command(message) -> bool:
    split_string = message.text.lower().split()
    if len(split_string) == 5:
        if split_string[0] == 'rename' and split_string[1] == 'subcategory' and split_string[3] == 'to':
            return True
    return False


def is_registration_command(message) -> bool:
    split_string = message.text.lower().split()
    if len(split_string) == 1:
        if split_string[0] == 'registration':
            return True
    return False


def get_help_message() -> str:
    help_list = [
        'Commands list:',
        '  Add category {category name},',
        '  Add subcategory {subcategory name} in {category name}',
        '  Delete category {category name}',
        '  Delete subcategory {subcategory name}',
        '  Show categories',
        '  Sow spends for {number of days} days in {category/subcategory name}',
        '  Draw pipe in {category name} for {number of days} days'
    ]
    result = ''
    for i in help_list:
        result += i + '\n'
    return result


def is_add_coin_command(message) -> bool:
    split_string = message.text.lower().split()
    if len(split_string) == 3:
        if split_string[0].isdigit() and split_string[1] == 'in':
            return True
    return False


def is_show_statistic_command(message) -> bool:
    # show statistic for 7 days
    # show statistic for 7 days in products
    split_string = message.text.lower().split()

    def check_1(split_string2):
        try:
            if len(split_string2) == 7 \
                    and split_string2[0] == 'show' \
                    and split_string2[1] == 'spends' \
                    and split_string2[2] == 'for' \
                    and split_string2[4] == 'days' or split_string2[4] == 'day' \
                    and split_string2[5] == 'in' \
                    and split_string2[3].isdigit():
                return True
        except Exception:
            return False

    def check_2(split_string2):
        try:
            if len(split_string2) == 5 \
                    and split_string2[0] == 'show' \
                    and split_string2[1] == 'spends' \
                    and split_string2[2] == 'for' \
                    and split_string2[3].isdigit():
                return True
        except Exception:
            return False

    if check_1(split_string) or check_2(split_string):
        return True
    return False


def is_draw_pipe_command(message) -> bool:
    split_string = message.text.lower().split()
    if len(split_string) == 7:
        if split_string[0] == 'draw'\
                and split_string[1] == 'pipe' \
                and split_string[2] == 'in' \
                and split_string[4] == 'for' \
                and split_string[5].isdigit() \
                and split_string[6] == 'days' or 'day':
            return True
    return False


def generate_token(length=10):
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(length))
    return token