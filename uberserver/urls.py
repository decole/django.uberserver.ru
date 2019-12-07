from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sensors/', views.sensors, name='sensors'),
    path('swifts/', views.swifts, name='swifts'),
    path('api/mqtt', views.mqttApi, name='api-mqtt'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    # path('activate/', views.activate, name='index'),
    path('logout/', views.logout_page, name='logout'),
]
