from django.urls import path
from . import views

urlpatterns = [
    path("ThreadList", views.ThreadList, name="ThreadList"),
    path("Thread", views.Thread, name="Thread")
]