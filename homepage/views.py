from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .models import *
from .forms import MovieForm, CustomRegisterForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib import messages
from django.db.models import Avg
from django.core.cache import cache


def homepage(request):
    movies = cache.get('homepage_movies')
    movies_rating = cache.get('homepage_movies_rating')
    movies_comment_count = cache.get('homepage_movies_comments')

    if not movies or not movies_rating:
        movies = Movie.objects.all()[:50]
        movies_rating = []
        movies_comment_count = []

        for obj in movies:
            avg_rating = Comment.objects.filter(movie=obj.movie_id).aggregate(Avg('rate'))['rate__avg'] or 0
            comment_count = Comment.objects.filter(movie=obj.movie_id).count()
            movies_comment_count.append(comment_count)
            movies_rating.append(int(avg_rating))

        cache.set('homepage_movies', movies, 600)
        cache.set('homepage_movies_rating', movies_rating, 600)
        cache.set('homepage_movies_comments', movies_comment_count, 600)

    movies_zip = zip(movies, movies_rating, movies_comment_count)
    watchlist_movies = []
    watchlist_zip = []


    if request.user.is_authenticated:
        watchlist_movies = Movie.objects.filter(watchlist__user=request.user.id)
        watchlist_movies_id = Watchlist.objects.filter(user_id=request.user.id)
        watchlist_zip = zip(watchlist_movies, watchlist_movies_id)

    return render(request, 'homepage.html', {
        'movies_zip': movies_zip,
        'movies': movies,
        'watchlist_movies': watchlist_movies,
        'watchlist_zip': watchlist_zip
    })

def homepage_specific_films(request):
    genre = request.GET.get('genre')
    movies = Movie.objects.filter(genre__icontains=genre)
    movies_rating = []
    watchlist_movies = []
    movies_comment_count = []

    for obj in movies:
        avg_rating = Comment.objects.filter(movie=obj.movie_id).aggregate(Avg('rate'))['rate__avg'] or 0
        comment_count = Comment.objects.filter(movie=obj.movie_id).count()
        movies_rating.append(int(avg_rating))
        movies_comment_count.append(comment_count)


    movies_zip = zip(movies, movies_rating, movies_comment_count)

    watchlist_movies = []
    watchlist_zip = []


    if request.user.is_authenticated:
        watchlist_movies = Movie.objects.filter(watchlist__user=request.user.id)
        watchlist_movies_id = Watchlist.objects.filter(user_id=request.user.id)
        watchlist_zip = zip(watchlist_movies, watchlist_movies_id)

    return render(request, 'homepage.html', {
        'movies_zip': movies_zip,
        'movies': movies,
        'watchlist_movies': watchlist_movies,
        'watchlist_zip': watchlist_zip
    })

@login_required
def add_watchlist(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    user = request.user

    if Watchlist.objects.filter(user=user, movie=movie).exists():
        messages.warning(request, 'Film już znajduje się na Twojej watchliście.')
    else:
        Watchlist.objects.create(user=user, movie=movie)
        messages.success(request, 'Film dodany do watchlisty.')

    return redirect('homepage')

def remove_watchlist(request, id):
    movie_watchlist = get_object_or_404(Watchlist, pk=id)

    if request.method == "POST":
        movie_watchlist.delete()
        return redirect('homepage')

@login_required
def show_watchlist(request):

    movies = cache.get('all_movies')
    movies_rating = cache.get('all_movies_ratings')
    movies_comment_count = cache.get('homepage_movies_comments')


    if not movies or not movies_rating:
        movies = list(Movie.objects.all())
        movies_rating = []

        for obj in movies:
            avg_rating = Comment.objects.filter(movie=obj.movie_id).aggregate(Avg('rate'))['rate__avg'] or 0
            comment_count = Comment.objects.filter(movie=obj.movie_id).count()
            movies_rating.append(int(avg_rating))
            movies_comment_count.append(comment_count)

        cache.set('all_movies', movies, 600)
        cache.set('all_movies_ratings', movies_rating, 600)
        cache.set('homepage_movies_comments', movies_comment_count, 600)

    watchlist_movies = Movie.objects.filter(watchlist__user=request.user.id)


    movies_zip = zip(watchlist_movies, movies_rating, movies_comment_count)
    watchlist_movies = []
    watchlist_zip = []


    if request.user.is_authenticated:
        watchlist_movies = Movie.objects.filter(watchlist__user=request.user.id)
        watchlist_movies_id = Watchlist.objects.filter(user_id=request.user.id)
        watchlist_zip = zip(watchlist_movies, watchlist_movies_id)

    return render(request, 'homepage.html', {
        'movies_zip': movies_zip,
        'movies': movies,
        'watchlist_movies': watchlist_movies,
        'watchlist_zip': watchlist_zip
    })

@login_required
def add(request):
    form = MovieForm(request.POST or None, request.FILES or None)
    previous_url = request.META.get('HTTP_REFERER', '/')
    if form.is_valid():
        form.save()
        return redirect(homepage)

    return render(request, 'new_form.html', {'form': form, 'previous_url': previous_url, 'action': "Create new film", 'title': "Dodaj nowy film"})


@login_required
def add_comment(request, id):
    form = CommentForm(request.POST or None)
    previous_url = request.META.get('HTTP_REFERER', '/')
    movie = Movie.objects.get(movie_id=id)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.movie = movie
        comment.save()
        return redirect('homepage')

    return render(request, 'new_form.html', {
        'form': form,
        'previous_url': previous_url,
        'action': "Add new commentary",
        'title': "Dodaj komentarz"
    })

@login_required
def edit(request, id):
    movie = get_object_or_404(Movie, pk=id)
    form = MovieForm(request.POST or None, request.FILES or None, instance=movie)
    previous_url = request.META.get('HTTP_REFERER', '/')

    if form.is_valid():
        form.save()
        return redirect(homepage)

    return render(request, 'new_form.html', {'form': form, 'previous_url': previous_url, 'action': f"Edit {movie.title}", 'title': f"Edytuj {movie.title}"})

@login_required
def delete(request, id):
    movie = get_object_or_404(Movie, pk=id)
    previous_url = request.META.get('HTTP_REFERER', '/')
    if request.method == "POST":
        movie.delete()
        return redirect(homepage)

    return render(request, 'delete.html', {'movie': movie, 'previous_url': previous_url, 'action': f"Remove {movie.title}"})

def login_view(request):

    next_url = request.GET.get('next') or request.POST.get('next')

    if request.user.is_authenticated:
        return redirect(homepage)

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            else:
                return redirect('homepage')

    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form, 'action': "Login"})

def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            messages.success(request, 'Konto zostało utworzone!')
            return redirect('login_view')
    else:
        form = CustomRegisterForm()
    return render(request, 'register.html', {'form': form})

def show_comments(request, id):
    comments = Comment.objects.filter(movie=id)
    movie_id = id
    print(comments)
    return render(request, 'comments.html', {'comments': comments, 'movie_id': movie_id})
