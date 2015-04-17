from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	return render(request, 'lab2/index.html', )

def authorize(request):
	return render(request, 'lab2/authorize.html', )


def register(request):
	return render(request, 'lab2/register.html', )

def register_post(request):
	return render(request, 'lab2/register_success.html',)