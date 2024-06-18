from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = ["<int:user_id>", views.Todos.as_view()]