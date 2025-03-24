from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *


def my_homepage(request):
    items = Movie.objects.all()
    return render(request, 'homepage/index.html', {'items': items})

def all_information(request):
    users = User.objects.all()
    return render(request, 'all_information/index.html', {'users': users})