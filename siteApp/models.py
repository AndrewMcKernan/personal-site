from django.db import models

# Create your models here.

class MainService(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Main Services"
    
class Technology(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Technologies"
    
class SubService(models.Model):
    name = models.CharField(max_length=200)
    main_service = models.ForeignKey(MainService, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Sub Services"