from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from lab2.models import Users, Apps, Token, Manufacturers, Devices
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
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
		if client_id == "" and response_type == "":
			return account(request)
		elif response_type == 'code':
			if client_id != None:
				try:
					app = Apps.objects.get(client_id=client_id)
					user_app = app.user
					if user.id == user_app.id:
						try:
							token = Token.objects.get(app_id=app)
							if not token.code_expired():
								token.delete()
								token = Token.create(app, redirect_uri)
								token.save()
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
			return redirect(request.path)
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

@csrf_exempt 
def token(request):
	if request.method == "POST":
		client_id = request.POST.get("client_id","")
		client_secret = request.POST.get("client_secret","")
		grant_type = request.POST.get("grant_type","")
		try:
			app = Apps.objects.get(client_id=client_id)
			if app.client_secret == client_secret:
				try:
					token = Token.objects.get(app_id=app)
					if grant_type == "authorization_code":
						code = request.POST.get("code","")
						redirect_uri = request.POST.get("redirect_uri","")
						res_json, error = issue_access_token(token, code, redirect_uri)
						if error == 0:
							return HttpResponse(res_json)
						else: 
							return HttpResponseBadRequest(res_json)
						
					elif grant_type == "refresh_token":
						refresh_token = request.POST.get("refresh_token","")
						if refresh_token == token.refresh_token:
							access_token, refresh_token, exp, token_type = token.create_token()
							token.save()
							return HttpResponse(json.dumps({"access_token": access_token,
												"refresh_token": refresh_token,
												"token_type": token_type,
												"expires": exp}),0)
						else:
							return HttpResponseBadRequest(json.dumps({'error': "invalid_request", 
												"info": "refresh_token is invalid"}))

					else:
						return HttpResponseBadRequest(json.dumps({'error': "invalid_request", 
												"info": "grant_type is invalid"}))

				except ObjectDoesNotExist:
						return HttpResponseBadRequest(json.dumps({'error': "invalid_request", 
										"info": "client_id and client_secret is invalid"}))
			else:
				return HttpResponseBadRequest(json.dumps({'error': "invalid_request", 
									"info": "client_secret is invalid"}))

		except ObjectDoesNotExist:
			return HttpResponseBadRequest(json.dumps({'error': "invalid_request", 
									"info": "client_id is invalid"}))

	return HttpResponse("token")

def issue_access_token(token, code, redirect_uri):
	if token.code == code:
		if token.code_expired():
			if token.access_token == None:
				if token.redirect_uri == redirect_uri:
					access_token, refresh_token, exp, token_type = token.create_token()
					token.save()
					return (json.dumps({"access_token": access_token,
										"refresh_token": refresh_token,
										"token_type": token_type,
										"expires": exp}),0)
				else:
					return (json.dumps({'error': "invalid_request", "info": "Uri doesn't match"}),1)
			else:
				return (json.dumps({"access_token": token.access_token,
										"refresh_token": token.refresh_token,
										"token_type": token.token_type,
										"expires": token.code_expires.strftime(settings.DATE_FORMAT)}),0)
		else:
			return (json.dumps({'error': "invalid_request","info": "code has expired"}),1)
	else:
		return (json.dumps({'error': "invalid_request", "info": "code is incorrect"}),1)

def account(request):
	if request.method == "GET":
		user = current_user(request)
		if user != None:
			app = user.apps_set.get()
			context = {"name": user.name,
						"client_id": app.client_id,
						"client_secret": app.client_secret}
		else:
			context = {"name": "None",
						"client_id": "None",
						"client_secret": "None"}
		return render(request, 'lab2/account.html', context)

def userinfo(request):
#	if request.method == "GET":

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
		try:
			user = Users.objects.get(pk=uid)
			return user
		except ObjectDoesNotExist:
			return None
	return None

def manufacturers(request):
	authorized = check_authorization(request)
	if authorized == 1:
		if request.method == "GET":
			data = []
			response_data = {}
			page = request.GET.get("page","")
			on_page = request.GET.get("on_page","")
			if page == "" and on_page == "":
				
				manufacturers = Manufacturers.objects.all()
				response_data["total_entries"] = Manufacturers.objects.count()
				
				i = 0
				for manufacturer in manufacturers:
					datal = {"id": manufacturer.id,
								"name": manufacturer.name,
								"established": manufacturer.established,
								"country": manufacturer.country}
					data.append(datal)
					i += 1
				response_data["entries"] = data
				return HttpResponse(json.dumps(response_data))
			else:
				try:
					page = int(page)
					on_page = int(on_page)
					manufacturers = Manufacturers.objects.all()
					count = Manufacturers.objects.count()
					first = on_page * (page-1)
					if first + 1 > count:
						return HttpResponseNotFound(json.dumps({"error": "invalid_request", "info": "Number of page is too big"}))
					if (first + on_page + 1) > count:
						last = first + on_page
					else:
						last = count - 1
					for i in range(first, last):
						manufacturer = manufacturers[i]
						datal = {"id": manufacturer.id,
								"name": manufacturer.name,
								"established": manufacturer.established,
								"country": manufacturer.country}
						data.append(datal)

					response_data["current_page"] = page
					response_data["on_page"] = on_page
					response_data["total_entries"] = count
					response_data["entries"] = data
					return HttpResponse(json.dumps(response_data))
				except ValueError:
					return HttpResponseBadRequest(json.dumps({"error": "invalid_request", "info": "page and on_page parameter are incorrect"}))
	elif authorized == 0:
		return HttpResponse(json.dumps({"error": "unauthorized"}), status=401)	
	else:
		return HttpResponse(json.dumps({"error": "token expired"}), status=401)

def man_detail(request, manufacturer_id):
	authorized = check_authorization(request)
	if authorized == 1:
		try:
			manufacturer = Manufacturers.objects.get(pk=manufacturer_id)
			return HttpResponse(json.dumps({"id": manufacturer.id,
											"name": manufacturer.name,
											"established": manufacturer.established,
											"country": manufacturer.country}))
		except ObjectDoesNotExist:
			return HttpResponseNotFound(json.dumps({"error": "Manufacturer with this ID is not found"}))
	elif authorized == 0:
		return HttpResponse(json.dumps({"error": "unauthorized"}), status=401)	
	else:
		return HttpResponse(json.dumps({"error": "token expired"}), status=401)

def devices(request):
	authorized = check_authorization(request)
	if authorized == 1:
		if request.method == "GET":
			data = []
			response_data = {}
			page = request.GET.get("page","")
			on_page = request.GET.get("on_page","")
			if page == "" and on_page == "":
				
				devices = Devices.objects.all()
				response_data["total_entries"] = Devices.objects.count()
				
				i = 0
				for device in devices:
					datal= {"id": device.id,
								"manufacturer": device.manufacturer.name,
								"name": device.name,
								"dig_disp": device.dig_disp,
								"device_type": device.device_type,
								"year": device.year}
					data.append(datal)
				response_data["entries"] = data
				return HttpResponse(json.dumps(response_data))
			else:
				try:
					page = int(page)
					on_page = int(on_page)
					devices = Devices.objects.all()
					count = Devices.objects.count()
					first = on_page * (page-1)
					if first + 1 > count:
						return HttpResponseNotFound(json.dumps({"error": "invalid_request", "info": "Number of page is too big"}))
					if (first + on_page + 1) > count:
						last = first + on_page
					else:
						last = count - 1
					for i in range(first, last):
						device = devices[i]
						datal = {"id": device.id,
											"manufacturer": device.manufacturer.name,
											"name": device.name,
											"dig_disp": device.dig_disp,
											"device_type": device.device_type,
											"year": device.year}
						data.append(datal)

					response_data["current_page"] = page
					response_data["on_page"] = on_page
					response_data["total_entries"] = count
					response_data["entries"] = data
					return HttpResponse(json.dumps(response_data))
				except ValueError:
					return HttpResponseBadRequest(json.dumps({"error": "invalid_request", "info": "page and on_page parameter are incorrect"}))
	elif authorized == 0:
		return HttpResponse(json.dumps({"error": "unauthorized"}), status=401)
	else:
		return HttpResponse(json.dumps({"error": "token expired"}), status=401)	

def dev_detail(request, device_id):
	authorized = check_authorization(request)
	if authorized == 1:
		try:
			device = Devices.objects.get(pk=device_id)
			return HttpResponse(json.dumps({"id": device.id,
											"manufacturer": device.manufacturer.name,
											"name": device.name,
											"dig_disp": device.dig_disp,
											"device_type": device.device_type,
											"year": device.year}))
		except ObjectDoesNotExist:
			return HttpResponseNotFound(json.dumps({"error": "Device with this ID is not found"}))
	elif authorized == 0:
		return HttpResponse(json.dumps({"error": "unauthorized"}), status=401)
	else:
		return HttpResponse(json.dumps({"error": "token expired"}), status=401)

def check_authorization(request):
	if request.method == "GET":
		authorization = request.META['HTTP_AUTHORIZATION']
		authorization = authorization.split(' ')
		if authorization[0] == "Bearer":
			try:
				token = Token.objects.get(access_token=authorization[1])
				if not token.token_expired():
					return -1
			except ObjectDoesNotExist:
				return 0		
		else:
			return 0
	return 1