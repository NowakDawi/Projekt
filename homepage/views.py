from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *
from .forms import MovieForm


def homepage(request):
    movies = Movie.objects.all()
    return render(request, 'homepage.html', {'movies': movies})

def add(request):
    form = MovieForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
    return render(request, 'new_form.html', {'form': form})
