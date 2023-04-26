from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("ThreadList", views.ThreadList, name="ThreadList"),
    path("ThreadList/<filter>", views.ThreadList, name="ThreadList"),
    path("<int:classId>/ThreadList", views.ThreadList, name="ThreadList"),
    path("Thread/<int:thread_id>/", views.Thread, name="Thread"),
    path("Classes",views.Classes,name='Classes'),
    path("Classes/<classNum>",views.Classes,name='ClassSearch'),
    path("CreateThread", views.CreateThread),
    path("uploadFile/", views.uploadFile,name="uploadFile"),
    path("LoginUser/<net_id>", views.LoginUser),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)