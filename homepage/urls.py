from django.urls import path
from . import views


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("add/", views.add, name="add"),
    path("edit/<int:id>/", views.edit,  name="edit"),
    path("delete/<int:id>/", views.delete, name="delete")
]
