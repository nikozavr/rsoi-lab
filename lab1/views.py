from django.shortcuts import render

from django.http import HttpResponse
# Create your views here.

def index(request):
	return render(request, 'lab1/index.html', )
#	return HttpResponse('Привет')

def code(request):
	return render(request, 'lab1/code.html', )
