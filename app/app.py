from flask import Flask, request
from flask_migrate import Migrate

from .models import db
from .api_routers import api_route
from .schedule_events import schedule_blue_print
from flask_cors import CORS
from .schedule_events import scheduler
from .telegram_handlers import telegram_webhook


class Config:
    SCHEDULER_API_ENABLED = True


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.config['PERMANENT_SESSION_LIFETIME'] = 360
    app.config['SESSION_COOKIE_HTTPONLY'] = False
    app.config['SESSION_COOKIE_SECURE'] = False
    app.register_blueprint(api_route)
    app.register_blueprint(schedule_blue_print)
    app.register_blueprint(telegram_webhook)

    db.init_app(app)
    migrate = Migrate(app, db)

    CORS(app)

    scheduler.start()


    @app.route('/', methods=['GET'])
    def webhook():

        if request.method == 'GET':
            return '<h1>Bot is working<h1>'

    return app
