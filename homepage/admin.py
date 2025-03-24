from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Movie)
admin.site.register(Cast)
admin.site.register(MovieCast)
admin.site.register(Watchlist)
admin.site.register(Comment)
