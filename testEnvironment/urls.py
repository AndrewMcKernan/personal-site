from django.urls import path

from . import views

app_name = "testEnvironment"

urlpatterns = [
    path('', views.index, name='index'),
]