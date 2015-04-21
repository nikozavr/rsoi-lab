from django.shortcuts import render
from django.http import HttpResponse
from lab2.models import Users
from django.core import serializers

import json

# Create your views here.
def index(request):
	return render(request, 'lab2/index.html', )

def auth(request):
	return render(request, 'lab2/authorize.html', )


def register(request):
	users = Users.objects.all();
	data = serializers.serialize('json', [ users, ])
	#users = serializers.serialize('json', self.get_queryset())
	users_json = json.dumps(dict(users));
	context = { 'users': data };
	return render(request, 'lab2/register.html', context)

def register_post(request):
	if request.method == "POST":
		user = Users(request.POST.get("login", ""),
					request.POST.get("email", ""),
					request.POST.get("name", ""),
					request.POST.get("phone", ""),
					request.POST.get("password",""));
		user.save()
		test = Users.objects.all()
		return HttpResponse(test)
	return render(request, 'lab2/register_success.html',)

def token(request):
	return HttpResponse("token")

def country(request):
	return HttpResponse("country")

def city(request):
	return HttpResponse("city")

def monument(request):
	return HttpResponse("monument")

def account(request):
	return HttpResponse("account")
