from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
  path("<int:user_id>", views.Todos.as_view()),
  path("<int:user_id>/<int:todo_id>", views.TodoDetail.as_view()),
  path("<int:user_id>/<int:todo_id>/check", views.TodoDetailCheck.as_view()),
  path("<int:user_id>/<int:todo_id>/reviews", views.TodoReview.as_view()),
]