from django.db import models

class ClientData(models.Model):
    client_id = models.CharField(max_length=200)
    client_secret = models.CharField(max_length=200)
#   initial = {'client_id': '41247-NWTAFVODdnE122H2muWJ',
#           'client_secret': 'qJoyFZ4uD6Yj0gsQA2xp'}

    def __str__(self):
        return self.client_id

# Create your models here.
class PersonalData(models.Model):
    code = models.CharField(max_length=10)
    access_token = models.CharField(max_length=200)
    token_type = models.CharField(max_length=50)
    expires_in = models.IntegerField(default=0)
    refresh_token = models.CharField(max_length=200)

    def __str__(self):
        return self.code