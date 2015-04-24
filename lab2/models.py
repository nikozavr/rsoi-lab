from django.db import models
from django.core.signing import Signer
from django.contrib.auth.hashers import make_password

import string
import random
import hashlib
from datetime import datetime, timedelta
from django.utils.timezone import utc
from django.conf import settings

class Users(models.Model):
	login = models.CharField(max_length=30)
	email = models.CharField(max_length=50)
	name = models.CharField(max_length=30)
	phone = models.CharField(max_length=20)
	password = models.CharField(max_length=100)

	def __str__(self):
		return self.login;

	@classmethod
	def create(cls, login, email, name, phone, password):
		password = make_password(password, None, 'md5')
		user = cls(login=login, email=email, name=name, phone=phone, password=password)
		return user


class Apps(models.Model):
    user = models.ForeignKey(Users)
    client_id = models.CharField(max_length=100, unique=True)
    client_secret = models.CharField(max_length=100, unique=True)

    @classmethod
    def create(cls, user):
        client_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
        client_secret = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
        app = user.apps_set.create(client_id=client_id, client_secret=client_secret)
        return app

class Token(models.Model):
	app_id = models.OneToOneField(Apps)
	code = models.CharField(max_length=100, unique=True)
	access_token = models.CharField(max_length=100, null=True)
	token_type = models.CharField(max_length=50, null=True)
	refresh_token = models.CharField(max_length=100,null=True)
	token_expires = models.DateTimeField(null=True)
	code_expires = models.DateTimeField(null=True)
	redirect_uri = models.CharField(max_length=100, null=True)

	@classmethod
	def create(cls, app, redirect_uri = None):
		now = datetime.utcnow().replace(tzinfo=utc)
		code_expires = now + timedelta(minutes = 10)
		string = app.client_id
		code = hashlib.sha224(string.encode('utf-8') + now.strftime(settings.DATE_FORMAT).encode('utf-8')).hexdigest()
		token = cls(app_id=app, code=code, code_expires=code_expires, redirect_uri=redirect_uri)
		return token

	def code_expired(self):
		return (self.code_expires - datetime.utcnow().replace(tzinfo=utc) > timedelta(seconds=0))

	def token_expired(self):
		return (self.token_expires - datetime.utcnow().replace(tzinfo=utc) > timedelta(seconds=0))

	def create_token(self):
		self.token_type = "Bearer"
		now = datetime.utcnow().replace(tzinfo=utc)
		self.token_expires = now + timedelta(minutes = 4)
		self.access_token = hashlib.sha224('access'.encode('utf-8') + self.code.encode('utf-8') + now.strftime(settings.DATE_FORMAT).encode('utf-8')).hexdigest()
		self.refresh_token = hashlib.sha224('refresh'.encode('utf-8') + self.code.encode('utf-8') + now.strftime(settings.DATE_FORMAT).encode('utf-8')).hexdigest()
		return (self.access_token, self.refresh_token, self.token_expires.strftime(settings.DATE_FORMAT), self.token_type)

class Manufacturers(models.Model):
	name = models.CharField(max_length=30)
	established = models.IntegerField()
	country = models.CharField(max_length=30)

class Devices(models.Model):
	manufacturer = models.ForeignKey(Manufacturers)
	name = models.CharField(max_length=100)
	device_type = models.CharField(max_length=50)
	dig_disp = models.FloatField()
	year = models.IntegerField()
