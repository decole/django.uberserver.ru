from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sensors/', views.sensors, name='sensors'),
    path('swifts/', views.swifts, name='swifts'),
    path('api/mqtt', views.mqttApi),
]
