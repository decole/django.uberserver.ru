from django.core.mail import send_mail


# Хелпер для отображения состояния умного дома
from uberserver.helpers.mqtt_helper import get_payload
from uberserver.models import Sensor


class StateSmartHome(object):
    @staticmethod
    def state_telegram():
        query_temperature = Sensor.objects.filter(type__type_name='sensor', format_sensor__format_name='temperature')
        query_humidity = Sensor.objects.filter(type__type_name='sensor', format_sensor__format_name='humidity')
        query_leakage = Sensor.objects.filter(type__type_name='leakage')

        message = ''
        for temperature in query_temperature:
            if get_payload(temperature.topic) is None:
                message = message + temperature.message_info + ": не имеет текущих данных \n"
            else:
                message = message + temperature.message_info + ": " + get_payload(temperature.topic) + "°C \n"

        for humidity in query_humidity:
            if get_payload(humidity.topic) is None:
                message = message + humidity.message_info + ": не имеет текущих данных \n"
            else:
                message = message + humidity.message_info + ": " + get_payload(humidity.topic) + '%' + "\n"

        for leakage in query_leakage:
            if get_payload(leakage.topic) is None:
                message = message + leakage.message_info + ": не имеет текущих данных \n"
            else:
                message = message + leakage.message_info + ': ' + get_payload(leakage.topic) + "\n"

        return "Состояние сенсоров:" + "\n" + message


    @staticmethod
    def state_alice():
        return 'Состояние сисемы: ок'
