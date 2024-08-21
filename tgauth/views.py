import re
import json
import base64

from django.shortcuts import render
from django.http import HttpResponse
from requests import get


def lfm_access_token(url_params):
    lfm_request = get(
        url='https://api2.lowfuelmotorsport.com/auth/steam/handle',
        params=url_params
    )
    match = r'(?<=data=).*?(?=&redirect)'
    lfm_raw = re.findall(match, lfm_request.url).pop()
    lfm_token = json.loads(
        base64.urlsafe_b64decode(lfm_raw + "=" * divmod(len(lfm_raw), 4)[1]).decode('utf-8')
    )['accessToken']

    return lfm_token


def auth(request):
    return render(request, 'auth.html')


def login(request):
    data = request.GET
    at = lfm_access_token(data)
    lfm_user = get(
        url='https://api2.lowfuelmotorsport.com/api/user',
        headers={'Authorization': 'Bearer ' + at}
    ).json()
    return HttpResponse()


def success(request):
    return HttpResponse('hello world')
