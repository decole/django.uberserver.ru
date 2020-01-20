from django.urls import path

from alice import views

urlpatterns = [
    path('', views.alice_api, name='alice-dialog'),
]
