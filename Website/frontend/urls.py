from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("ThreadList", views.ThreadList, name="ThreadList"),
    path("Classes/<int:classId>/ThreadList", views.ThreadList, name="ThreadList"),
    path("<int:classId>/ThreadList", views.ThreadList, name="ThreadList"),
    path("Thread/<int:thread_id>/", views.Thread, name="Thread"),
    path("Classes",views.Classes,name='Classes'),
    path("Classes/<classNum>",views.Classes,name='ClassSearch'),
    path("CreateThread", views.CreateThread),
    path("<int:classId>/ThreadList/uploadFile/", views.uploadFile,name="uploadFile"),
    path("<int:classId>/uploadFile", views.uploadFile,name="uploadFile")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)