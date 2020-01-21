from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError
from uberserver.models import Sensor, Type, Weather
import requests, json


class Command(BaseCommand):
    help = 'cache test'

    def handle(self, *args, **options):
        # //cache.set('underground/temperature', 'lol', 30)
        rest = 'margulis/temperature'
        sensors_list_cache = Sensor.objects.values()
        # type_sensor = Type.objects.get(type_name="sensor")
    #    sensors_list = Sensor.objects.filter(type__type_name='sensor').values()
        # print(type_sensor)
    #    print(sensors_list)
        # var = cache.get('mqtt_list_sensors')
        # print(var)
        # print(sensors_list)
        # for sensor in sensors_list_cache:
        #     if rest == sensor['topic']:
        #         print('sensor --')
        ''' http://apidev.accuweather.com/currentconditions/v1/291309.json?language=ru-ru&apikey=hoArfRosT1215 '''
        try:
            res = requests.get("http://apidev.accuweather.com/currentconditions/v1/291309.json?language=ru-ru&apikey=hoArfRosT1215")
            # data = json.dumps(res.json())
            data = res.json()
            time = str(data[0]['EpochTime'])
            weather_text = str(data[0]['WeatherText'])
            temperature = str(data[0]['Temperature']['Metric']['Value'])
            # MqttPayload(topic=res['topic'], payload=res['payload']).save()
            Weather(text=weather_text, temperature=temperature).save()
            print()
        except Exception as e:
            print("Exception (weather):", e)
            pass
