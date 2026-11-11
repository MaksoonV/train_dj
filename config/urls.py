"""Все адреса сайта начинаются здесь."""
from django.urls import include, path

urlpatterns = [path("", include("tasks.urls"))]
