from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.decorators import login_required
from kvetchupapp import models
from users.models import User

import requests


def register(request):
    message = request.GET.get('message', '')
    context = {
        'message': message
    }
    return render(request, 'users/register.html', context)

def register_user(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']

    if User.objects.filter(username=username).exists():
        return HttpResponseRedirect(reverse('users:register') + '?message=exists')

    user = User.objects.create_user(username, email, password)
    login(request, user)

    return HttpResponseRedirect(reverse('kvetchupapp:index'))


def login_page(request):
    message = request.GET.get('message', '')
    next = request.GET.get('next', '')
    context = {
        'next': next,
        'message': message
    }
    return render(request, 'users/login.html', context)


def login_user(request):

    next = request.POST['next']

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        if next != '':
            return HttpResponseRedirect(next)
        return HttpResponseRedirect(reverse('kvetchupapp:index'))
    if next == '':
        return HttpResponseRedirect(reverse('users:login') + '?message=failure')
    return HttpResponseRedirect(reverse('users:login') + '?message=failure&next='+next)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('kvetchupapp:index') + '?message=True')

@login_required
def home(request):
    return render(request, 'users/home.html')