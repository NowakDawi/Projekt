from django.urls import path
from . import views


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("find_movies/", views.homepage_specific_films, name="find_movie"),
    path("add/", views.add, name="add"),
    path("add_watchlist/<int:movie_id>/", views.add_watchlist, name="add_watchlist"),
    path("show_watchlist/", views.show_watchlist, name="show_watchlist"),
    path("register/", views.register, name="register"),
    path("edit/<int:id>/", views.edit,  name="edit"),
    path("delete/<int:id>/", views.delete, name="delete"),
    path("delete_watchlist/<int:id>/", views.remove_watchlist, name="remove_watchlist")
]
