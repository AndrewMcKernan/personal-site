from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.db.models.functions import Lower
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import HttpResponse
from django.core.exceptions import ValidationError

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

def sendEmail(request):
    
    if request.method == "POST":
        sender_email = request.POST['email']
        sender_message = request.POST['message']
        sender_name = request.POST['name']
        sender_service = request.POST['service']
        message = "Sender Name: " + sender_name + "\n\n" + \
                "Sender Email: " + sender_email + "\n\n" + \
                "Requested Service: " + sender_service + "\n\n" + \
                "Message: " + sender_message
        try: 
            validate_email(sender_email)
        except ValidationError:
            #messages.error(request, 'The given email address is invalid.')
            return HttpResponse(status=400)
        send_mail(
                'Website Form Submission Received From ' + sender_name, # Subject
                message, # Message
                "do-not-reply@andrewmckernan.ca", # from email
                ["andrewmck96@gmail.com"], # to email
                fail_silently=False,
            )
        return HttpResponse(status=200)