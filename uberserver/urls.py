from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sensors/', views.sensors, name='sensors'),
    # path('swifts/', views.swifts, name='swifts'),
    path('margulis/', views.swifts_margulis, name='margulis'),
    path('watering/', views.swifts_water, name='watering'),
    path('swifts_kitchen/', views.swifts_kitchen, name='kitchen'),
    path('api/mqtt', views.mqtt_api, name='api-mqtt'),
    path('api/mqtt/get', views.mqtt_api_get, name='api-mqtt-get'),
    path('api/mqtt/post', views.mqtt_api_post, name='api-mqtt-post'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    # path('activate/', views.activate, name='index'),
    path('logout/', views.logout_page, name='logout'),
]
