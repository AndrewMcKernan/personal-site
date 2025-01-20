from django.db import models


# Create your models here.
class CoreTokens(models.Model):
    _singleton = models.BooleanField(default=True, editable=False, unique=True)
    state = models.CharField(max_length=36)
    waiting_for_tokens = models.BooleanField(default=False)
    token_request_code = models.CharField(max_length=50)  # I'm not sure how long this code needs to be
    access_token = models.CharField(max_length=100)
    access_token_expiry = models.DateTimeField()
    refresh_token = models.CharField(max_length=100)
    refresh_token_expiry = models.DateTimeField()
