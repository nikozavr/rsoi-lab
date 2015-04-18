from django.shortcuts import render
from django.http import HttpResponse
from lab2.models import Users

# Create your views here.
def index(request):
	return render(request, 'lab2/index.html', )

def authorize(request):
	return render(request, 'lab2/authorize.html', )


def register(request):
	return render(request, 'lab2/register.html', )

def register_post(request):
	if request.method == "POST":
		user = Users(request.POST.get("login", ""),
					request.POST.get("email", ""),
					request.POST.get("name", ""),
					request.POST.get("phone", ""),
					request.POST.get("password",""));
		return HttpResponse(user);
	return render(request, 'lab2/register_success.html',)