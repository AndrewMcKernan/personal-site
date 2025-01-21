from django.shortcuts import render, redirect
from .core_api import *

# Create your views here.


def index(request):
    return render(request, "testEnvironment/index.html")


def request_new_tokens(request):
    result = get_authorization_code_uri()
    return redirect(result)


def auth_callback(request):
    get_access_token(request)
    print("Auth Callback")
    return redirect("testEnvironment:index")


def request_refresh_token(request):
    result = get_refresh_code_uri()
    return redirect(result)


def refresh_auth_callback(request):
    get_refresh_token(request)
    print("Refresh Auth Callback")
    return redirect("testEnvironment:index")
