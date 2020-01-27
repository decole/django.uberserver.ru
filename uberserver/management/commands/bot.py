import logging
import requests

from django.core.management.base import BaseCommand
from django.conf import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from uberserver.helpers.mqtt_helper import post_payload
from uberserver.helpers.state_system_helper import StateSmartHome

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('''
/set <seconds> поставить таймер
/unset - отмена таймера 
/lampOn - включить лампу
/lampOff - выключить лампу
/alarm - тестовое сообщение
/weather - погода сейчас AcuWeather
/secureOn - включить систему безопасности
/secureOff - выключить систему безопасности
/sensors
    ''')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def alarm(update, context):
    """Send the alarm message."""
    update.message.reply_text('Beep!')


def set_timer(update, context):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        # Add job to queue and stop current one if there is a timer already
        if 'job' in context.chat_data:
            old_job = context.chat_data['job']
            old_job.schedule_removal()
        new_job = context.job_queue.run_once(alarm, due, context=chat_id)
        context.chat_data['job'] = new_job

        update.message.reply_text('Timer successfully set!')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def unset(update, context):
    """Remove the job if the user changed their mind."""
    if 'job' not in context.chat_data:
        update.message.reply_text('You have no active timer')
        return

    job = context.chat_data['job']
    job.schedule_removal()
    del context.chat_data['job']

    update.message.reply_text('Timer successfully unset!')


def lamp_on(update, context):
    topic = 'margulis/lamp01'
    payload = 'on'
    post_payload(topic, payload)
    update.message.reply_text('Дампа включена')


def lamp_off(update, context):
    topic = 'margulis/lamp01'
    payload = 'off'
    post_payload(topic, payload)
    update.message.reply_text('Дампа выключена')


def weather(update, context):
    try:
        res = requests.get("http://apidev.accuweather.com/currentconditions/v1/291309.json?language=ru-ru&apikey=hoArfRosT1215")
        data = res.json()
        # time = str(data[0]['EpochTime'])
        weather_text = str(data[0]['WeatherText'])
        temperature = str(data[0]['Temperature']['Metric']['Value'])
        return update.message.reply_text('Сейчас погода в Камышине: ' + temperature + 'C`' + weather_text)
    except Exception as e:
        return update.message.reply_text("Exception (weather):", e)


def secure_on(update, context):
    topic = 'home/security/cocking'
    payload = '1'
    post_payload(topic, payload)
    return update.message.reply_text('Охранная система перешла в дежурный режим')


def secure_off(update, context):
    topic = 'home/security/cocking'
    payload = '0'
    post_payload(topic, payload)
    return update.message.reply_text('Охранная система отключена')


def sensors(update, context):
    return update.message.reply_text(StateSmartHome.state_telegram())


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        REQUEST_KWARGS = {
            'proxy_url': settings.PROXY_URL,
            # Optional, if you need authentication:
            'urllib3_proxy_kwargs': {
                'username': settings.PROXY_LOGIN,
                'password': settings.PROXY_PASSWORD,
            }
        }
        updater = Updater(settings.TELEGRAM_TOKEN, use_context=True,
                          request_kwargs=REQUEST_KWARGS)

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help))
        dp.add_handler(CommandHandler("set", set_timer,
                                      pass_args=True,
                                      pass_job_queue=True,
                                      pass_chat_data=True))
        dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))
        dp.add_handler(CommandHandler("alarm", alarm))
        dp.add_handler(CommandHandler("lampOn", lamp_on))
        dp.add_handler(CommandHandler("lampOff", lamp_off))
        dp.add_handler(CommandHandler("weather", weather))
        dp.add_handler(CommandHandler("secureOn", secure_on))
        dp.add_handler(CommandHandler("secureOff", secure_off))
        dp.add_handler(CommandHandler("sensors", sensors))

        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(Filters.text, echo))

        # log all errors
        dp.add_error_handler(error)

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()
