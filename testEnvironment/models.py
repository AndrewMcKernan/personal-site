from django.db import models


# Create your models here.
class CoreTokens(models.Model):
    _singleton = models.BooleanField(default=True, editable=False, unique=True)
    state = models.CharField(max_length=36, blank=True)
    waiting_for_tokens = models.BooleanField(default=False)
    token_request_code = models.CharField(max_length=50, blank=True)  # I'm not sure how long this code needs to be
    access_token = models.CharField(max_length=100, blank=True)
    access_token_expiry = models.DateTimeField()
    refresh_token = models.CharField(max_length=100, blank=True)
    refresh_token_expiry = models.DateTimeField()
