from django.db import models

# Create your models here.

class MainService(models.Model):
    name = models.CharField(max_length=200)
    
class Technology(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/images/')
    
class Subservice(models.Model):
    name = models.CharField(max_length=200)
    main_service = models.ForeignKey(MainService, on_delete=models.CASCADE)
    technologies = models.ManyToManyField(Technology)