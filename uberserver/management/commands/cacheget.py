# manage.py mqtt - starting command
# pip install paho-mqtt
import sys

from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError


import paho.mqtt.subscribe as subscribe


from uberserver.helpers.mqtt_helper import on_message_print


class Command(BaseCommand):
    help = 'cache test'

    def handle(self, *args, **options):
        cache.set('underground/temperature', 'lol', 30)
        var = cache.get('underground/temperature')
        print(var)
