from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from lab2.models import Users, Apps
from django.core import serializers

from django.contrib.auth.hashers import make_password, check_password
import json

# Create your views here.
def index(request):
	return render(request, 'lab2/index.html', )

def auth(request):
	user = current_user()
	if request.method == "GET" and user is not None:
		client_id = request.GET.get("client_id","")
		redirect_uri = request.GET.get("redirect_uri","")
		response_type = request.GET.get("response_type","")
		if response_type is not None and response_type == 'code':
			if client_id is not None:
				client = Client.query.filter_by(client_id=client_id).first()
				if client.user_id == user.id:
					if client is not None:
						token = Token.query.filter_by(client_id=client.id).first()
						if token is None:
							token = Token(client.id, client_id, redirect_uri)
							db.session.add(token)
							db.session.commit()
						elif token.code_expired():
							db.session.delete(token)
							token = Token(client.id, client_id, redirect_uri)
							db.session.add(token)
							db.session.commit()
						if redirect_uri is not None:
							return redirect(redirect_uri + '?code=' + token.code)
						else:
							return json.dumps({'code' : token.code})
				else:
					return 'Incorrect credentials: mismatch of client and user'
			return 'Inocrrect credentials: client_id is required'
		else:
			return 'Incorrect response_type: value of response_type must be code'
	if request.method == "GET" and user is None:
		return render(request, 'lab2/authorize.html', )
	if request.method == "POST":
		error_text = ""
		login = request.POST.get("login", "")
		password = request.POST.get("password", "")
		try:
			user = Users.objects.get(login=login)
			if check_password()
		except Users.DoesNotExist:
			error_text = "Ошибка входа"

		if error_text == "":
			app = user.apps_set.get()
			context = {"name": user.name,
					"client_id": app.client_id,
					"client_secret": app.client_secret}
			return render(request, 'lab2/account.html', context)
		else:
			return render(request, 'lab2/authorize.html', {"error_text": error_text})

def auth_check(request):
	error_text = ""
	if request.method == "POST":
		login = request.POST.get("login", "")
		password = request.POST.get("password", "")
		try:
			user = Users.objects.get(login=login)
		except Users.DoesNotExist:
			error_text = "Ошибка входа"

	if error_text == "":
		app = user.apps_set.get()
		context = {"name": user.name,
					"client_id": app.client_id,
					"client_secret": app.client_secret}
		return render(request, 'lab2/account.html', context)
	else:
		return render(request, 'lab2/authorize.html', {"error_text": error_text})

def register(request):
	users = Users.objects.all();
	logins = list(users.values_list('login', flat = True))
	emails = list(users.values_list('email', flat = True))
	context = { 'logins': logins, 'emails': emails }
	return render(request, 'lab2/register.html', context)

def register_post(request):
	if request.method == "POST":
		user = Users.create(request.POST.get("login", ""),
							request.POST.get("email", ""),
							request.POST.get("name", ""),
							request.POST.get("phone", ""),
							request.POST.get("password", ""),)
		user.save()
		app = Apps.create(user)
		app.save()
	return render(request, 'lab2/register_success.html', )

def token(request):
	return HttpResponse("token")

def country(request):
	return HttpResponse("country")

def city(request):
	return HttpResponse("city")

def monument(request):
	return HttpResponse("monument")

def account(request):
	return render(request, 'lab2/account.html', )
def userinfo(request):
	return HttpResponse("userinfo")


def current_user(request):
	if 'id' in request.session:
		uid = request.session['id']
		return Users.objects.get(pk=uid)
	return None
