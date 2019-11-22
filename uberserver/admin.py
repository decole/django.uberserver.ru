from django.contrib import admin
from . import models


admin.site.register(models.Link)
admin.site.register(models.Type)
admin.site.register(models.Format)
admin.site.register(models.Sensor)
admin.site.register(models.Swift)
admin.site.register(models.TelegramUser)
