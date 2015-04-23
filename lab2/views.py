from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from lab2.models import Users, Apps, Token
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist


from django.contrib.auth.hashers import make_password, check_password
import json

# Create your views here.
def index(request):
	return render(request, 'lab2/index.html', )

def auth(request):
	user = current_user(request)
	if request.method == "GET" and user != None:
		client_id = request.GET.get("client_id","")
		redirect_uri = request.GET.get("redirect_uri","")
		response_type = request.GET.get("response_type","")
		if response_type == 'code':
			if client_id != None:
				try:
					app = Apps.objects.get(client_id=client_id)
					user_app = app.user
					if user.id == user_app.id:
						try:
							token = Token.objects.get(app_id=app)
							if token.code_expired():
								token.delete()
								token = Token.create(app, redirect_uri)
								tokeb.save()
						except ObjectDoesNotExist:
							token = Token.create(app, redirect_uri)
							token.save()

						if redirect_uri != None:
							return redirect(redirect_uri + '?code=' + token.code)
						else:
							return json.dumps({'code' : token.code})
					else:
						return HttpResponseBadRequest(json.dumps({'error': "invalid_request", 
											"info": "client_id is not correct"}))
				except ObjectDoesNotExist:
						return HttpResponseBadRequest(json.dumps({'error': "invalid_request", 
											"info": "client_id is not correct"}))
			return HttpResponseBadRequest(json.dumps({'error': "invalid_request", 
										"info": "client_id is required"}))
		else:
			return HttpResponseBadRequest(json.dumps({'error': "invalid_request", 
										"info": "value of response_type must be code"}))
	if request.method == "GET" and user is None:

		return render(request, 'lab2/authorize.html', )
	if request.method == "POST":
		error_text = ""
		login = request.POST.get("login", "")
		password = request.POST.get("password", "")
		try:
			user = Users.objects.get(login=login)
			if check_password(password, user.password) == False:
				error_text = "Неправильный пароль"
			else:
				request.session['id'] = user.id
		except Users.DoesNotExist:
			error_text = "Ошибка входа"

		if error_text == "":
			app = user.apps_set.get()
			context = {"name": user.name,
					"client_id": app.client_id,
					"client_secret": app.client_secret}
			return redirect(request.url)
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
	if request.method == "POST":
		code = request.POST.get("code","")
		client_id = request.POST.get("client_id","")
		client_secret = request.POST.get("client_secret","")
		redirect_uri = request.POST.get("redirect_uri","")
		grant_type = request.POST.get("grant_type","")
		if grant_type == "grant_type":
			try:
				app = Apps.objects.get(client_id=client_id)
				if app.client_secret == client_secret:
					try:
						token = Token.objects.get(app_id=app)
					except ObjectDoesNotExist:
						return 
				else:
					return HttpResponseBadRequest(json.dumps({'error': "invalid_request", 
										"info": "client_secret is invalid"}))

			except ObjectDoesNotExist:
				return HttpResponseBadRequest(json.dumps({'error': "invalid_request", 
										"info": "client_id is invalid"}))

		else:
			return HttpResponseBadRequest(json.dumps({'error': "invalid_request", 
										"info": "grant_type must be grant_type"}))			

	return HttpResponse("token")

def country(request):
	return HttpResponse("country")

def city(request):
	return HttpResponse("city")

def monument(request):
	return HttpResponse("monument")

def account(request):
	user = current_user(request)
	app = user.apps_set.get()
	context = {"name": user.name,
				"client_id": app.client_id,
				"client_secret": app.client_secret}
	return render(request, 'lab2/account.html', context)

def userinfo(request):
	return HttpResponse("userinfo")

def logout(request):
	try:
		del request.session['id']
	except KeyError:
		pass
	return HttpResponse("Вы вышли")

def current_user(request):
	if 'id' in request.session:
		uid = request.session['id']
		return Users.objects.get(pk=uid)
	return None
