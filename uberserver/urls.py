from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sensors/', views.sensors, name='sensors'),
    path('swifts/', views.swifts, name='swifts'),
    path('api/mqtt', views.mqttApi, name='api-mqtt'),
    path('login/', views.login, name='index'),
    path('register/', views.register, name='index'),
    path('activate/', views.activate, name='index'),
    path('logout/', views.logout, name='index'),
]
