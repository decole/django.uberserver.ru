from django.db import models


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


class Sensor(models.Model):
    name = models.CharField(max_length=200)
    condition_min = models.IntegerField()
    condition_max = models.IntegerField()
    message_info = models.CharField(max_length=200, null=True)
    message_ok = models.CharField(max_length=200, null=True)
    message_alarm = models.CharField(max_length=200, null=True)
    message_danger = models.CharField(max_length=200, null=True)
    topic = models.CharField(max_length=200)
    notify_users = models.CharField(max_length=1000, null=True)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    format_sensor = models.ForeignKey(Format, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    link = models.ForeignKey(Link, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Swift(models.Model):
    name = models.CharField(max_length=200)
    topic_on = models.CharField(max_length=20)
    topic_off = models.CharField(max_length=20)
    message_info = models.CharField(max_length=200, null=True)
    message_on = models.CharField(max_length=200, null=True)
    message_off = models.CharField(max_length=200, null=True)
    message_danger = models.CharField(max_length=200, null=True)
    topic = models.CharField(max_length=200)
    topic_check = models.CharField(max_length=200)
    topic_check_on = models.CharField(max_length=20)
    topic_check_off = models.CharField(max_length=20)
    notify_users = models.CharField(max_length=1000, null=True)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    format_swift = models.ForeignKey(Format, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    link = models.ForeignKey(Link, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
