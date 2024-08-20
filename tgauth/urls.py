from django.contrib import admin
from django.urls import path, include
from .views import auth, login, success

urlpatterns = [
    path('auth/', auth, name='auth'),
    path('login/', login, name='login'),
    path('success/', success, name='success')
]
