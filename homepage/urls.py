from django.urls import path
from . import views

urlpatterns = [
    path("", views.my_homepage, name="homepage"),
    path("all_information/", views.all_information, name="all_information")
]