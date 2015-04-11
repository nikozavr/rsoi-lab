from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'lab2/index.html', )


def register(request):
	return render(request, 'lab2/register.html', )