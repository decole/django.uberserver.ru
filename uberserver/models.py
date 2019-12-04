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
