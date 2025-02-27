from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Movie)
admin.site.register(MovieCast)
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(Watchlist)
