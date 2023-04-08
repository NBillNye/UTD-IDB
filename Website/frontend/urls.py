from django.urls import path, include
from . import views

urlpatterns = [
    path("ThreadList", views.ThreadList, name="ThreadList"),
    path("<int:classId>/ThreadList", views.ThreadList, name="ThreadList"),
    path("Thread/<int:thread_id>/", views.Thread, name="Thread"),
    path("Classes",views.Classes,name='Classes'),
    path("Classes/<classNum>",views.Classes,name='ClassSearch')
]