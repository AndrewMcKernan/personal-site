from django.shortcuts import render, redirect
from .core_api import *

# Create your views here.


def index(request):
    return render(request, "testEnvironment/index.html")


def request_new_tokens():
    get_authorization_code()
    return redirect("testEnvironment:index")


def auth_callback(request):
    get_refresh_and_access_tokens(request)
    print("Auth Callback")
    return redirect("testEnvironment:index")