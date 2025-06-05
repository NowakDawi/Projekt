from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    description = models.TextField()
    genre = models.TextField(max_length=100, default='')
    poster = models.ImageField(upload_to='poster/', null=True, blank=True)

    def __str__(self):
        return self.title

class Cast(models.Model):
    actor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    birth_date = models.DateField()
    description = models.TextField()

class MovieCast(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Cast, on_delete=models.CASCADE)

class Watchlist(models.Model):
    watchlist_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField(null=False)
    rate = models.IntegerField(default=1, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])

class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)