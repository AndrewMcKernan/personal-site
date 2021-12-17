from django.shortcuts import render, get_object_or_404, redirect
from .models import *

# Create your views here.

def index(request):
    mainServices = MainService.objects.all()
    subServices = SubService.objects.all()
    technologies = Technology.objects.all()
    context = {
        'mainServices':mainServices,
        'subServices':subServices,
        'technologies':technologies,
    }
    return render(request, "siteApp/index.html", context)