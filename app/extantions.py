import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from .config import token

#Telegram bot
bot = telebot.TeleBot(token)

#Apscheduler
scheduler = BackgroundScheduler()
