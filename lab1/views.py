from django.shortcuts import render
from django.http import HttpResponse
from lab1.models import ClientData, PersonalData

import requests, json
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

    post_data = {'grant_type': 'authorization_code',
                'code': personal_data_code.code,
                'redirect_uri': 'http%3A%2F%2Flocalhost%3A8000%2Flab1%2Ftoken%2F',
                'client_id': ClientData.objects.get(id=1).client_id,
                'client_secret': ClientData.objects.get(id=1).client_secret
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    r = requests.post("https://webapi.teamviewer.com/api/v1/oauth2/token/", data=post_data, headers=headers)
    result = r.json()

 #   personal_data_code.access_token = result["access_token"]
 #   personal_data_code.token_type = result["token_type"]
 #   personal_data_code.expires_in = result["expires_in"]
 #   personal_data_code.refresh_token = result["refresh_token"]

  #  personal_data_code.save()

    return HttpResponse(result["access_token"])

def gettoken(request):
    return HttpResponse('Success')
