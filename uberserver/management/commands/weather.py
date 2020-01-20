from django.core.management.base import BaseCommand
from uberserver.models import  Weather
import requests


class Command(BaseCommand):
    help = 'save weather in DB'

    def handle(self, *args, **options):
        try:
            res = requests.get("http://apidev.accuweather.com/currentconditions/v1/291309.json?language=ru-ru&apikey=hoArfRosT1215")
            data = res.json()
            # time = str(data[0]['EpochTime'])
            weather_text = str(data[0]['WeatherText'])
            temperature = str(data[0]['Temperature']['Metric']['Value'])
            Weather(text=weather_text, temperature=temperature).save()
        except Exception as e:
            print("Exception (weather):", e)
            pass
