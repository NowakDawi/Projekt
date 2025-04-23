from django.urls import path
from . import views


urlpatterns = [
    path("all/", views.homepage),
    path("add/", views.add),
]
