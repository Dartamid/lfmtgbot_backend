from django.shortcuts import render
from django.http import HttpResponse


def auth(request):
    return render(request, 'auth.html')


def login(request):
    return HttpResponse('hello world')


def success(request):
    return HttpResponse('hello world')
