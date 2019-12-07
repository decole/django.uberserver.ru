# Хелпер для работы с mqtt протоколом и датчиками
#
# проверить нет ли в cache параметров и топиков
# если нет параметров грузим с БД параметры, так же если давно не присылались сообщения с микросервиса
# тоже грузимся с БД,
# если есть параметры и топики приходят известные, то проверяем топики по присланным данным
# если приходят топики которых нет, записать их в кэш параметр который потом будет использоваться для проверок
#
# проверка на аварийность данных
# проверка на доступность контроллеров
# проверка на незарегистрированные топики
# функция отправки команд микроконтроллерам
from datetime import datetime
from django.core.cache import cache
from uberserver_django.settings import env
from uberserver.models import Sensor, Swift, MqttPayload


def analise(res):
    param = cache.get('mqtt_param_last_update')  # последнее обновление конфигурации
    param_site = cache.get('site_param_last_update')  # последнее обновление конфига датчиков на сайте
    if not param or not param_site:
        reset_cache()
    if param and param_site:
        if param_site > param:
            reset_cache()
            # print('refresh analise config, because site config change')
    if not cache.get('mqtt_list_sensors') or not cache.get('mqtt_list_swifts'):
        refresh_config_sensors()
        refresh_config_swifts()
        # sensors_list = Sensor.objects.filter(type__type_name='sensor').values()
        # swifts_list = Swift.objects.filter(type__type_name='swift').values()
        # cache.set('mqtt_list_sensors', sensors_list)
        # cache.set('mqtt_list_swifts', swifts_list)

    sensors_list_cache = cache.get('mqtt_list_sensors')
    swifts_list_cache = cache.get('mqtt_list_swifts')
    for sensor in sensors_list_cache:
        if sensor['topic'] == res['topic']:
            save_to_db(sensor, res)
            payload = round(float(res['payload']))
            sensor_min = round(sensor['condition_min'])
            sensor_max = round(sensor['condition_max'])
            if payload < sensor_min or payload > sensor_max:
                alarm(res)
    for swift in swifts_list_cache:
        if swift['topic'] == res['topic']:
            change_state(res)
            save_message_payload(res)
        if swift['topic_check'] == res['topic']:
            # проверка с состоянием на контрольной точке
            check_swift_state(res)
    cache.set(res['topic'], res['payload'], 60)


def reset_cache():
    date = round(datetime.today().timestamp())
    cache.set('mqtt_param_last_update', date, 86400)
    cache.set('site_param_last_update', date, 86400)
    cache.set('mqtt_list_sensors', '')
    cache.set('mqtt_list_swifts', '')


def alarm(res):
    print('alarm! sensor ' + res['topic'] + ' data is not ok (' + res['payload'] + ')')
#     @Todo отправить на почту сообщение и в телеграм


def save_to_db(obj, res):
    # print(obj)
    now = round(datetime.today().timestamp())
    date = round(datetime.today().timestamp())
    cache_topic = cache.get('cache_'+obj['topic'])
    if not cache_topic:
        cache.set('cache_'+obj['topic'], date, 3600)
        cache_topic = date
    if (now - int(env('SAVE_ON_SECONDS'))) > cache_topic:
        cache.set('cache_' + obj['topic'], date, 3600)
        save_message_payload(res)


def save_message_payload(res):
    MqttPayload(topic=res['topic'], payload=res['payload']).save()


def change_state(res):
    swifts_list_cache = cache.get('mqtt_list_swifts')
    #  change state swift on db
    for swift in swifts_list_cache:
        if res['topic'] == swift['topic']:
            payload = translate_swift_payload(res['payload'])
            model = Swift.objects.get(topic=swift['topic'])
            model.state = int(payload)
            model.save()
    refresh_config_swifts()


def check_swift_state(res):
    swifts_list_cache = cache.get('mqtt_list_swifts')
    for swift in swifts_list_cache:
        if res['topic'] == swift['topic_check']:
            # print('find check state')
            model = Swift.objects.get(topic=swift['topic'])
            payload = translate_swift_payload(res['payload'])
            if str(model.state) != str(payload):
                print(str(model.state) + ' ' + str(payload))
                print('аномалии в работе реле ' + model.name)
                #  @Todo информировать о аномалиях в топике реле


def refresh_config_swifts():
    swifts_list = Swift.objects.filter(type__type_name='swift').values()
    cache.set('mqtt_list_swifts', swifts_list)


def refresh_config_sensors():
    sensors_list = Sensor.objects.filter(type__type_name='sensor').values()
    cache.set('mqtt_list_sensors', sensors_list)


def translate_swift_payload(payload):
    if payload == 'on':
        payload = 1
    if payload == 'off':
        payload = 0
    return payload
