# manage.py mqtt - starting command
# pip install paho-mqtt
from django.core.management.base import BaseCommand, CommandError
from uberserver.helpers.mqtt_helper import on_message_print
import paho.mqtt.subscribe as subscribe


class Command(BaseCommand):
    help = 'mqtt client from django app'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Mqtt client is starting'))
        subscribe.callback(on_message_print, "#", hostname="uberserver.ru", port=2223)
