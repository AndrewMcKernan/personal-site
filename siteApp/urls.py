from django.urls import path

from . import views

app_name = "siteApp"

urlpatterns = [
    path('', views.index, name='index'),
    path('sendEmail', views.sendEmail, name="sendEmail"),
]