from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
import requests


class Command(BaseCommand):
    help = 'тест отправкисообщения через бота'

    def handle(self, *args, **options):
        # text = 'hi, bot is send message'
        # token = settings.TELEGRAM_TOKEN
        # url = "https://api.telegram.org/bot"
        # channel_id = "245579764"
        # url += token
        # method = url + "/sendMessage"
        # requests.post(method, data={
        #     "chat_id": channel_id,
        #     "text": text
        # }, proxies=dict(https='socks5://decole:wkyeGuVT@185.219.83.21:1080'))
        send_mail(
            subject='Notification Uberserver.ru - Test',
            message='Это тестовое сообшение',
            from_email='decole2014@yandex.ru',
            recipient_list=['decole@rambler.ru'],
            fail_silently=False
        )
