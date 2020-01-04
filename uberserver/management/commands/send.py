from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.utils.request import Request


class Command(BaseCommand):
    help = 'тест отправкисообщения через бота'

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            request=request,
            token=settings.TELEGRAM_TOKEN,
            base_url=settings.PROXY_URL,
        )
        REQUEST_KWARGS = {
            'proxy_url': 'socks5://185.219.83.21:1080',
            # Optional, if you need authentication:
            'urllib3_proxy_kwargs': {
                'username': 'decole',
                'password': 'wkyeGuVT',
            }
        }
        chat_id = 245579764
        bot.send_message(chat_id=chat_id, text="I'm sorry Dave I'm afraid I can't do that.")
