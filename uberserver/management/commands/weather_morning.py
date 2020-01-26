from django.core.management.base import BaseCommand
from django.conf import settings
import requests

from uberserver.helpers.telegram_helper import send_telegram_message


class Command(BaseCommand):
    help = 'отправка в телеграм сообщения о погоде'

    def handle(self, *args, **options):
        try:
            res = requests.get(
                "http://apidev.accuweather.com/currentconditions/v1/291309.json?language=ru-ru&apikey=hoArfRosT1215")
            data = res.json()
            weather_text = str(data[0]['WeatherText'])
            temperature = str(data[0]['Temperature']['Metric']['Value'])
            send_telegram_message('Сейчас погода в Камышине: ' + temperature + 'C`' + weather_text)
        except Exception as e:
            print("Exception (weather):", e)
            pass
