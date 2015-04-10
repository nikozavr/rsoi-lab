from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404, JsonResponse
from lab1.models import ClientData, PersonalData

import requests, json
# Create your views here.

def index(request):
    client_data = ClientData.objects.get(id=1)
    context = {'client_data': client_data}
    return render(request, 'lab1/index.html', context)

def getcode(request):
    if PersonalData.objects.all().count() != 0:
        personal_data_d = PersonalData.objects.all()[0]
        personal_data_d.delete()

    personal_data_code = PersonalData(code=request.GET.get('code',''))
    personal_data_code.save()

    return redirect('http://localhost:8000/lab1/result/')


def getresult(request):
    personal_data_code = PersonalData.objects.all()[0]

    post_data = {'grant_type': 'authorization_code',
                'code': personal_data_code.code,
                'redirect_uri': 'http%3A%2F%2Flocalhost%3A8000%2Flab1%2Fresult%2F',
                'client_id': ClientData.objects.get(id=1).client_id,
                'client_secret': ClientData.objects.get(id=1).client_secret
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    r = requests.post("https://webapi.teamviewer.com/api/v1/oauth2/token/", data=post_data, headers=headers)
    result = r.json()

    try:
        personal_data_code.access_token = result["access_token"]
        personal_data_code.token_type = result["token_type"]
        personal_data_code.expires_in = result["expires_in"]
        personal_data_code.refresh_token = result["refresh_token"]
        personal_data_code.save()
        return JsonResponse(PersonalData.get_account(personal_data_code.access_token, personal_data_code.token_type))
    except KeyError as error:
 #       return HttpResponseNotFound('<h1>Page not found(404)</h1><p><a href = "http://localhost:8000/lab1/>Back</a></p>')
        raise Http404(result["error"])

def gettoken(request):
    return HttpResponse('Success')
