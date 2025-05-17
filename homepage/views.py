from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .models import *
from .forms import MovieForm
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme

def homepage(request):
    movies = Movie.objects.all()
    return render(request, 'homepage.html', {'movies': movies})

@login_required
def add(request):
    form = MovieForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect(homepage)

    return render(request, 'new_form.html', {'form': form})

@login_required
def edit(request, id):
    movie = get_object_or_404(Movie, pk=id)
    form = MovieForm(request.POST or None, request.FILES or None, instance=movie)
    previous_url = request.META.get('HTTP_REFERER', '/')

    if form.is_valid():
        form.save()
        return redirect(homepage)

    return render(request, 'new_form.html', {'form': form, 'previous_url': previous_url})

@login_required
def delete(request, id):
    movie = get_object_or_404(Movie, pk=id)
    previous_url = request.META.get('HTTP_REFERER', '/')
    if request.method == "POST":
        movie.delete()
        return redirect(homepage)

    return render(request, 'delete.html', {'movie': movie, 'previous_url': previous_url})

def login_view(request):

    next_url = request.GET.get('next') or request.POST.get('next')

    if request.user.is_authenticated:
        return redirect(homepage)  # or whatever your home/dashboard URL is

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # return redirect(homepage)

            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            else:
                return redirect('homepage')

    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})
