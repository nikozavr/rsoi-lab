from django.shortcuts import render

from django.http import HttpResponse

from lab1.models import ClientData, PersonalData
# Create your views here.

def index(request):
    client_data = ClientData.objects.get(id=1)
    context = {'client_data': client_data}
    return render(request, 'lab1/index.html', context)
#   return HttpResponse('Привет')

def code(request):
    return render(request, 'lab1/code.html', )

def getcode(request):
    if PersonalData.objects.all().count() != 0:
        personal_data_d = PersonalData.objects.all()[0]
        personal_data_d.delete()

    personal_data_code = PersonalData(code=request.GET.get('code',''))
    personal_data_code.save()
    return render(request, 'lab1/getcode.html', )
