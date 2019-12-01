from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError

from uberserver.models import Sensor, Type


class Command(BaseCommand):
    help = 'cache test'

    def handle(self, *args, **options):
        # //cache.set('underground/temperature', 'lol', 30)
        rest = 'margulis/temperature'
        sensors_list_cache = Sensor.objects.values()
        # type_sensor = Type.objects.get(type_name="sensor")
        sensors_list = Sensor.objects.filter(type__type_name='sensor').values()
        # print(type_sensor)
        print(sensors_list)
        # var = cache.get('mqtt_list_sensors')
        # print(var)
        # print(sensors_list)
        # for sensor in sensors_list_cache:
        #     if rest == sensor['topic']:
        #         print('sensor --')
