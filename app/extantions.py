import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from .config import settings

#Telegram bot
bot = telebot.TeleBot(settings.token)

#Apscheduler
scheduler = BackgroundScheduler()
