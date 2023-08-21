import datetime
from functools import wraps
from flask import request, jsonify, session, Response
from .extantions import bot
from .logger import logger
from .queries_to_db import ApiQueries
from .service import check_hash_password, generate_token
from flask import Blueprint, current_app
from .models import db, RegistrationModel
import jwt
import json

api_route = Blueprint('api', __name__, url_prefix='/api')

def check_username_and_password(password, username):
    def get_user_hash_password(username):

        with current_app.app_context():
            get_hash_password = db.engine.execute(
                'SELECT hash_password FROM "registrariton" WHERE username=%s ',
                (username))

            hash_password = []

            for row in get_hash_password:
                hash_password.append(row[0])

            return hash_password[0]

    if check_hash_password(password, get_user_hash_password(username)) is True:
        return True


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        cookies = request.headers['Cookie'].split(' ')
        token_slice = len('coin_bot_token=')
        token = [item for item in cookies if item.lower().startswith('coin_bot_token=')][0][token_slice:-1]
        
        if str(token) == "null" or not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])

        except:
            return jsonify({'message': 'token is invalid'})

        return f(data['public_id'], *args, **kwargs)

    return decorator


@api_route.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '<h1>Api is working<h1>'
    if request.method == 'POST':
        try:
            r = request.get_json()
            if check_username_and_password(r['password'], r['username']) is True:
                user = RegistrationModel.query.filter_by(username=r['username']).first()
                token = jwt.encode(
                    {'public_id': user.telegram_user, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=45)},
                    current_app.config['SECRET_KEY'], "HS256")

                return jsonify({"token": token}), 200
            else:
                return jsonify({"responce": "Invalid password or username"}), 401

        except Exception:
            return jsonify({"responce": "Invalid password or username"}), 401


@api_route.route('/users/categories', methods=['GET'])
@token_required
def get_all_user_categories(user_id):
    try:

        data = ApiQueries().user_categories(user_id, current_app.app_context())
        return jsonify(data)

    except Exception as exc:
        logger.exception('An error occurred: %s', str(exc))
        return jsonify('Server error'), 500


@api_route.route('/users/subcategories', methods=['GET'])
@token_required
def get_all_user_subcategories(user_id):
    try:

        data = ApiQueries().get_user_subcategories(user_id, current_app.app_context())
        return jsonify(data)

    except Exception as exc:
        logger.exception('An error occurred: %s', str(exc))
        return jsonify('Server error'), 500


@api_route.route('/users/categories/income', methods=['GET'])
@token_required
def get_all_user_spent_categories(user_id):
    try:

        data = ApiQueries().get_user_income_categories(user_id, 2, current_app.app_context())
        return jsonify(data)

    except Exception as exc:
        logger.exception('An error occurred: %s', str(exc))
        return jsonify('Server error'), 500


@api_route.route('/users/subcategories/income', methods=['GET'])
@token_required
def get_all_user_spent_subcategories(user_id):
    try:
        data = ApiQueries().get_user_income_subcategories(user_id, 2, current_app.app_context())
        return jsonify(data)
    except Exception as exc:
        logger.exception('An error occurred: %s', str(exc))
        return jsonify('Server error'), 500


@api_route.route('/users/categories/spent', methods=['GET'])
@token_required
def get_all_user_income_categories(user_id):
    try:
        data = ApiQueries().get_user_income_categories(user_id, 1, current_app.app_context())
        return jsonify(data)
    except Exception as exc:
        logger.exception('An error occurred: %s', str(exc))
        return jsonify('Server error'), 500


@api_route.route('/users/subcategories/spent', methods=['GET'])
@token_required
def get_all_user_income_subcategories(user_id):
    try:
        data = ApiQueries().get_user_income_subcategories(user_id, 1, current_app.app_context())
        return jsonify(data)
    except Exception as exc:
        logger.exception('An error occurred: %s', str(exc))
        return jsonify('Server error'), 500


@api_route.route('/users/categories/<category_name>/coins', methods=["GET"])
@token_required
def get_coins_per_category(user_id, category_name):
    try:
        args = request.args
        data = ApiQueries().count_sum_coins_per_period_per_category(user_id,
                                                                    category_name,
                                                                    args.get('date_range'),
                                                                    args.get('start_date'),
                                                                    args.get('finish_date'),
                                                                    current_app.app_context())
        return jsonify(data)
    except Exception as exc:
        logger.exception('An error occurred: %s', str(exc))
        return jsonify('Server error'), 500


@api_route.route('/users/subcategories/<subcategory_name>/coins', methods=["GET"])
@token_required
def get_coins_per_subcategory(user_id, subcategory_name):
    try:
        args = request.args
        data = ApiQueries().count_sum_coins_per_period_per_subcategory(user_id,
                                                                       subcategory_name,
                                                                       args.get('date_range'),
                                                                       args.get('start_date'),
                                                                       args.get('finish_date'),
                                                                       current_app.app_context())
        return jsonify(data)
    except Exception as exc:
        logger.exception('An error occurred: %s', str(exc))
        return jsonify('Server error'), 500


@api_route.route('/users/date_registration', methods=["GET"])
@token_required
def get_user_date_registration(user_id):
    try:
        data = ApiQueries().get_user_date_registration(user_id, current_app.app_context())
        return jsonify(data)
    except Exception as exc:
        logger.exception('An error occurred: %s', str(exc))
        return jsonify('Server error'), 500


@api_route.route('/users/income/coins', methods=["GET"])
@token_required
def get_user_income_coins(user_id):
    try:
        args = request.args
        data = ApiQueries().get_all_coins(user_id,
                                          args.get('date_range'),
                                          args.get('start_date'),
                                          args.get('finish_date'),
                                          2,
                                          current_app.app_context())
        return jsonify(data)
    except Exception as exc:
        logger.exception('An error occurred: %s', str(exc))
        return jsonify('Server error'), 500


@api_route.route('/users/spent/coins', methods=["GET"])
@token_required
def get_user_spent_coins(user_id):
    try:
        args = request.args
        data = ApiQueries().get_all_coins(user_id,
                                          args.get('date_range'),
                                          args.get('start_date'),
                                          args.get('finish_date'),
                                          1,
                                          current_app.app_context())
        return jsonify(data)
    except Exception as exc:
        logger.exception('An error occurred: %s', str(exc))
        return jsonify('Server error'), 500


@api_route.route('/handle_user', methods=['POST'])
def handle_password():
    try:
        method = request.method
        url = request.url
        headers = request.headers
        data = request.get_data(as_text=True)

        token = generate_token()

        # session[str(request.form['google_id'])] = [token, request.form['user_id']]

        with open('test_data.json', 'w') as json_file:
            data = {str(request.form['google_id']):[token, request.form['user_id']]}
            json.dump(data, json_file)

        bot.send_message(request.form['user_id'], 'your token is')
        bot.send_message(request.form['user_id'], token)

        responce = Response('Succes', status=200)

        return responce

    except Exception as exc:
        logger.exception('An error occurred: %s', str(exc))
        return jsonify('Server error'), 500


@api_route.route('/check_token', methods=['POST'])
def handle_token():

    try:

        token = request.form['token']
        google_id = request.form['google_id']

        # token_in_session = session[google_id]

        with open('test_data.json', 'r') as json_file:
            # Загрузка данных из файла
            data = json.load(json_file)
            token_in_session = data[str(google_id)]

        print('token ', token)
        print('token in session', token_in_session)


        if token == token_in_session[0]:
            enter_token = jwt.encode(
                        {'public_id': token_in_session[1],
                        'additional_data': 'coin_bot'},
                        current_app.config['SECRET_KEY'],
                        "HS256")

            data = {
                'token': enter_token,
                'bot_id' : 1
            }


            return jsonify(data)
        else:
            return 'Invalid token'
    
    except Exception as exc:
        logger.exception('An error occurred: %s', str(exc))
        return jsonify('Server error'), 500
