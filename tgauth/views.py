import re
import json
import base64

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from requests import get
from .models import BotUser


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
    if BotUser.objects.filter(tg_id=data['tg_id']).exists():
        return HttpResponse('User already authorized!')
    BotUser.objects.create(tg_id=data['tg_id'], access_token=at)
    response = redirect('success')
    response.set_cookie('tg_id', data['tg_id'])
    return response


def success(request, tg_id=None):
    try:
        tg_id = request.COOKIES['tg_id']
    except KeyError:
        return redirect('auth')
    user = get_object_or_404(BotUser, tg_id=tg_id)
    lfm_user = get(
        url='https://api2.lowfuelmotorsport.com/api/user',
        headers={'Authorization': 'Bearer ' + user.access_token}
    ).json()
    return render(
        request,
        template_name='success.html',
        context={
            'avatar': lfm_user['avatar'],
            'user_fullname': f'{lfm_user["vorname"]} {lfm_user["nachname"]}',
            'safety_rating': lfm_user['safety_rating'],
            'elo_rating': lfm_user['rating_by_sim'][0]['rating']
        }
    )
