from django.urls import re_path, path
from . import views
from . import API

urlpatterns = [
    path('', views.index, name='index'),
    path('user/<int:user_id>', API.GetUserInformation, name="GetUserInformation"),
    path('threads/GetThreadList/<int:user_id>/', API.GetThreadList, name="GetThreadList")
]