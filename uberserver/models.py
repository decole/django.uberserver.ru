import datetime

from django.db import models
from django.urls import reverse
from django.utils import timezone


def default_time():
    return timezone.now() + datetime.timedelta(hours=4)


class Link(models.Model):
    link_name = models.CharField(max_length=200)

    def __str__(self):
        return self.link_name


class Type(models.Model):
    type_name = models.CharField(max_length=200)

    def __str__(self):
        return self.type_name


class Format(models.Model):
    format_name = models.CharField(max_length=200)
    format_symbol = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.format_name


class TelegramUser(models.Model):
    name = models.CharField(max_length=200)
    telegram_id = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.name


class Sensor(models.Model):
    name = models.CharField(max_length=200, help_text='Название')
    condition_min = models.IntegerField(help_text='Минимальные значения')
    condition_max = models.IntegerField(help_text='Максимальные значения')
    message_info = models.CharField(max_length=200, null=True, help_text='Информация о сенсоре')
    message_ok = models.CharField(max_length=200, null=True, help_text='Когда все ок')
    message_alarm = models.CharField(max_length=200, null=True, help_text='Сигнальная информация')
    message_danger = models.CharField(max_length=200, null=True, help_text='Сообщение об аварии')
    topic = models.CharField(max_length=200, help_text='Топик MQTT')
    notify_users = models.ManyToManyField(TelegramUser, help_text='Пользователи telegram')
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    format_sensor = models.ForeignKey(Format, on_delete=models.CASCADE, help_text='Формат')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, help_text='Тип')
    link = models.ForeignKey(Link, on_delete=models.CASCADE, help_text='Ссылка на объект')

    def __str__(self):
        # return str(self.name + ' ( ' + self.topic + ' )')
        # return '{1} - {0}'.format(self.name, self.topic)
        return '{name} - ( {topic} )'.format(name=self.name, topic=self.topic)

    def get_sensor_data(self):
        return {
            'id': self.id,
            'name': self.name,
            'topic': self.topic,
            'condition_min': self.condition_min,
            'condition_max': self.condition_max,
            'link': self.link.link_name,
            'link_id': self.link.id,
        }

    def get_absolute_url(self):
        return reverse('sensor_detail', args=[str(self.id)])


class Swift(models.Model):
    name = models.CharField(max_length=200, help_text='Название')
    topic_on = models.CharField(max_length=20, help_text='Значение \'on\'')
    topic_off = models.CharField(max_length=20, help_text='Значение \'off\'')
    message_info = models.CharField(max_length=200, null=True, help_text='Информация о сенсоре')
    message_on = models.CharField(max_length=200, null=True, help_text='Сообщение при вклчении')
    message_off = models.CharField(max_length=200, null=True, help_text='Сообщение при выклчении')
    message_danger = models.CharField(max_length=200, null=True, help_text='Сообщение при неисправностях')
    topic = models.CharField(max_length=200, help_text='Топик MQTT')
    topic_check = models.CharField(max_length=200, help_text='Проверочный топик MQTT')
    topic_check_on = models.CharField(max_length=20, help_text='Значение \'on\'')
    topic_check_off = models.CharField(max_length=20, help_text='Значение \'off\'')
    notify_users = models.ManyToManyField(TelegramUser, help_text='Пользователи telegram')
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    format_swift = models.ForeignKey(Format, on_delete=models.CASCADE, help_text='Формат')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, help_text='Тип')
    link = models.ForeignKey(Link, on_delete=models.CASCADE, help_text='Ссылка на объект')
    state = models.IntegerField(help_text='Состояние переключателя', default=0)

    def __str__(self):
        # str_format = 'влажность в пристройке - {value} %'
        # return str_format.format(value = self.name)
        return '{name} - {{ {topic} }}'.format(name=self.name, topic=self.topic)

    def get_swift_data(self):
        return {
            'id': self.id,
            'name': self.name,
            'topic': self.topic,
            'topic_check': self.topic_check,
            'link': self.link.link_name,
            'link_id': self.link.id,
        }

    def get_absolute_url(self):
        return reverse('swift_detail', args=[str(self.id)])


class MqttPayload(models.Model):
    topic = models.CharField(max_length=200, null=False)
    payload = models.CharField(max_length=400, null=False)
    datetime = models.DateTimeField(default=default_time)

    def __str__(self):
        return self.topic


# Сообщения для воркера, который будет отправлять данные по расписанию
class NotifyMessage(models.Model):
    EMAIL = 'EM'
    TELEGRAM = 'TE'
    SITE = 'SI'
    NOTIFY_CHOICES = [
        (EMAIL, 'email'),
        (TELEGRAM, 'telegram'),
        (SITE, 'site'),
    ]
    profile_notify = models.CharField(max_length=2, choices=NOTIFY_CHOICES, default=EMAIL)
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(verbose_name='Время получения', auto_now_add=True)
    done = models.BooleanField(default=0, verbose_name='статус сообщения')

    def __str__(self):
        return f'{self.profile_notify} | Сообщение {self.pk} - {self.done}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения нотификации'


class Weather(models.Model):
    text = models.CharField(max_length=255, verbose_name='Текс')
    temperature = models.FloatField(verbose_name='Температура')
    datetime = models.DateTimeField(verbose_name='Дата съема показаний', default=default_time)


class Scheduler(models.Model):
    command = models.CharField(max_length=255, verbose_name='Команда')
    date_start = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, verbose_name='Начало')
    date_end = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name='Окончание')
    periodic = models.CharField(null=True, max_length=255, verbose_name='Параметр периодичности')
    active = models.BooleanField(null=True, default=0, verbose_name='Активно')

    def __str__(self):
        return f'Задача {self.command} от {self.date_start} | {self.periodic} - {self.active}'

    def get_scheduler_data(self):
        return {
            'id': self.id,
            'command': self.command,
            'date_start': self.date_start,
            'date_end': self.date_end,
            'periodic': self.periodic,
            'active': self.active,
        }

    class Meta:
        verbose_name = 'задача'
        verbose_name_plural = 'Планировщик задач'


class ScheduleTaskHistory(models.Model):
    task = models.CharField(max_length=255, verbose_name='Команда')
    datetime_start = models.DateTimeField(default=default_time, verbose_name='Запущена')
    state = models.BooleanField(null=True, default=0, verbose_name='Состояние')

    class Meta:
        verbose_name = 'Выполненная задача'
        verbose_name_plural = 'Планировщик задач - История'

    def __str__(self):
        return f'Задача {self.task} от {self.datetime_start} - {self.state}'


class SmartHomeSystemObject(models.Model):
    # состояние сенсоров (все ли постоянно обновляются)
    # состояние полива
    # состояние охранной системы
    # состояние пожарной системы

    SENSOR = 'SE'
    WATERING = 'WA'
    SECURITY = 'SC'
    FIRE_SECURITY = 'SF'

    NOTIFY_CHOICES = [
        (SENSOR, 'sensor'),
        (WATERING, 'watering'),
        (SECURITY, 'security'),
        (FIRE_SECURITY, 'fire_security'),
    ]

    name = models.CharField(max_length=255, verbose_name='Название')
    current_message = models.CharField(max_length=255, verbose_name='Кратко')
    state = models.BooleanField(null=True, default=0, verbose_name='Состояние')
    type = models.CharField(max_length=2, choices=NOTIFY_CHOICES, default=SENSOR)
    message_ok = models.CharField(max_length=255, verbose_name='Сообщение - норма')
    message_warning = models.CharField(max_length=255, verbose_name='Сообщение - авария')
    last_update = models.DateTimeField(auto_now=False, blank=False, verbose_name='Последнее сообщение')

    class Meta:
        verbose_name = 'Модуль системы'
        verbose_name_plural = 'Моули умного дома'

    def __str__(self):
        return f'Система {self.name} {self.type} - {self.state} {self.state}'


class ControllerState(models.Model):
    name = models.CharField(max_length=255, verbose_name='Контроллер')
    location = models.CharField(max_length=255, verbose_name='Где находится')
    prevent_topic = models.CharField(max_length=200, null=False)  # топик, который будет использоваться для проверки
    last_update = models.DateTimeField(auto_now=True, blank=False, verbose_name='Последнее сообщение')
    message_ok = models.CharField(max_length=200, null=True, help_text='Когда все ок')
    message_alarm = models.CharField(max_length=200, null=True, help_text='Сигнальная информация')
    state = models.BooleanField(null=True, default=0, verbose_name='Состояние')
    link = models.ForeignKey(Link, on_delete=models.CASCADE, help_text='Ссылка на объект')

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Состояние контроллеров'

    def __str__(self):
        return f'Контроллер {self.name} - {self.state}'


class SecuritySensor(models.Model):
    name = models.CharField(max_length=255, verbose_name='Извещатель')
    location = models.CharField(max_length=255, verbose_name='Где находится')
    topic = models.CharField(max_length=200, null=False)
    message_ok = models.CharField(max_length=200, null=True, help_text='Когда все ок')
    message_alarm = models.CharField(max_length=200, null=True, help_text='Сигнальная информация')
    state = models.BooleanField(null=True, default=0, verbose_name='Состояние')
    link = models.ForeignKey(Link, on_delete=models.CASCADE, help_text='Ссылка на объект')
    toggle = models.BooleanField(null=True, default=0, verbose_name='Взведение')

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Охранная система'

    def __str__(self):
        return f'Извещатель {self.name} ({self.topic}) - Состояние:{self.state} взведение:{self.toggle}'


class FireSecuritySystem(models.Model):
    name = models.CharField(max_length=255, verbose_name='Извещатель')
    location = models.CharField(max_length=255, verbose_name='Где находится')
    topic = models.CharField(max_length=200, null=False)
    message_ok = models.CharField(max_length=200, null=True, help_text='Когда все ок')
    message_alarm = models.CharField(max_length=200, null=True, help_text='Сигнальная информация')
    state = models.BooleanField(null=True, default=0, verbose_name='Состояние')
    link = models.ForeignKey(Link, on_delete=models.CASCADE, help_text='Ссылка на объект')
    toggle = models.BooleanField(null=True, default=0, verbose_name='Взведение')

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Пожарная система'

    def __str__(self):
        return f'Извещатель {self.name} ({self.topic}) - Состояние:{self.state} взведение:{self.toggle}'
