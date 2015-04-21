from django.db import models
from django.core.signing import Signer

class Users(models.Model):
	login = models.CharField(max_length=30)
	email = models.CharField(max_length=50)
	name = models.CharField(max_length=30)
	phone = models.CharField(max_length=20)
	password = models.CharField(max_length=100)
#	apps = models.ForeignKey(Apps)

	def __str__(self):
		return self.login;

	def __init__(self, login, email, name, phone, password):
		self.login = login
		self.email = email
		self.name = name
		self.phone = phone
		self.password = password

	#def as_json(self):
    #	return dict(login = self.login, email = self.email, name = self.name, phone = self.phone)

class Apps(models.Model):
	user = models.ForeignKey(Users)
	client_id = models.CharField(max_length=100, unique=True)
	secret_id = models.CharField(max_length=100, unique=True)

	def __init__(self, user):
		user = user
		self.client_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))
		self.client_secret = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))

class Token(models.Model):
	client_id = models.OneToOneField(Apps, primary_key=True)
	code = models.CharField(max_length=100, unique=True)
	access_token = models.CharField(max_length=100)
	refresh_token = models.CharField(max_length=100)
	token_expires = models.DateField()
	code_expires = models.CharField(max_length=30)
	redirect_uri = models.CharField(max_length=100)

	def __init__(self, client_id, client_id_str, redirect_uri = None):
		self.client_id = client_id
		now = datetime.utcnow()
		self.code_expires = now + timedelta(minutes = 5)
		self.code = hashlib.sha224(client_id_str + now.strftime(DATE_FORMAT)).hexdigest()
		self.redirect_uri = redirect_uri		

	def __repr__(self):
		return 'id: %d, client_id: %d, code: %s, expires: %s, redirect_uri: %s, access: %s, refresh:%s' % (self.id, self.client_id, self.code, self.code_expires.strftime(DATE_FORMAT), self.redirect_uri, self.access_token, self.refresh_token)

	def code_expired(self):
		return not (self.code_expires - datetime.utcnow() > timedelta(seconds=0))

	def token_expired(self):
		return not (self.token_expires - datetime.utcnow() > timedelta(seconds=0))

	def create_tokens(self):
		now = datetime.utcnow()
		self.token_expires = now + timedelta(minutes = 4)
		self.access_token = hashlib.sha224('access' + self.code + now.strftime(DATE_FORMAT)).hexdigest()
		self.refresh_token = hashlib.sha224('refresh' + self.code + now.strftime(DATE_FORMAT)).hexdigest()
		return (self.access_token, self.refresh_token, self.token_expires.strftime(DATE_FORMAT))

	
class Country(models.Model):
	name = models.CharField(max_length=30)

class City(models.Model):
	country = models.ForeignKey(Country)
	name = models.CharField(max_length=30)

class Monument(models.Model):
	city = models.ForeignKey(City)
	name = models.CharField(max_length=30)
	date = models.DateField()
