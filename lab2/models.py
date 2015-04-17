from django.db import models
from django.core.signing import Signer

class User(models.Model):
	username = models.CharField(max_length=30)
	email = models.CharField(max_length=50)
	name = models.CharField(max_length=30)
	phone = models.CharField(max_length=20)
	password = models.CharField(max_length=100)
	
