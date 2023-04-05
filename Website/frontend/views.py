from django.shortcuts import render
import requests
from decouple import config
from . import models as db

# Create your views here.

def ThreadList(response):
    threads = db.Thread.objects.all()
    if threads is not None:
        return render(response, 'ThreadList/index.html', {"threads": threads})
    return render(response, "ThreadList/index.html", {})

def Thread(response, thread_id=-1):
    if thread_id != -1:
        thread = db.Thread.objects.filter(threadid = thread_id).first()
        if thread is not None:
            return render(response, 'Thread/index.html', {"thread": thread})

    return render(response, 'Thread/index.html', {"title": "This is a test title"})

def Classes(response):
    classesL = db.Class.objects.all()
    if classesL is not None:
        return render(response, 'Classes/index.html', {"Classes": classesL})
    return render(response, "Classes/index.html", {})