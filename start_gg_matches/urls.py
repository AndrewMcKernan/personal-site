from django.urls import path

from . import views

app_name = "start_gg_matches"

urlpatterns = [
    path('', views.index, name='index'),
]