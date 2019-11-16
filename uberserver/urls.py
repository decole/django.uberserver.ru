from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sensors/', views.sensors, name='sensors'),
    path('sensor/<int:id_sensor>', views.sensor, name='sensor'),
    path('swifts/', views.swifts, name='swifts'),
    path('swift/<int:id_swift>', views.swift, name='swift'),
]
