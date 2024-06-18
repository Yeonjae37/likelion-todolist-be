from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
  path("<int:user_id>", views.Todos.as_view())
]