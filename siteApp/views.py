from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.db.models.functions import Lower

# Create your views here.

def index(request):
    mainServices = MainService.objects.order_by('order')
    subServices = SubService.objects.order_by(Lower('name'))
    technologies = Technology.objects.order_by(Lower('name'))
    context = {
        'mainServices':mainServices,
        'subServices':subServices,
        'technologies':technologies,
    }
    return render(request, "siteApp/index.html", context)