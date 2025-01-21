from django.urls import path

from . import views

app_name = "testEnvironment"

urlpatterns = [
    path('', views.index, name='index'),
    path('request_new_tokens', views.request_new_tokens, name='request_new_tokens'),
    path('request_refresh_token', views.request_refresh_token, name='request_refresh_token'),
    path('callback', views.auth_callback, name='callback'),
    path('refreshCallback', views.refresh_auth_callback, name='refreshCallback'),
]