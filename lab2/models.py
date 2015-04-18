from django.db import models
from django.core.signing import Signer

class Users(models.Model):
	login = models.CharField(max_length=30)
	email = models.CharField(max_length=50)
	name = models.CharField(max_length=30)
	phone = models.CharField(max_length=20)
	password = models.CharField(max_length=100)

	def __str__(self):
		return self.login;
	
