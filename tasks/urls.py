from django.urls import path
from . import views

app_name = "tasks"
urlpatterns = [
    path("", views.index, name="index"),
    path("tasks/<int:pk>/toggle/", views.toggle, name="toggle"),
    path("tasks/<int:pk>/delete/", views.delete, name="delete"),
]
