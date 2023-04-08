from django.shortcuts import render
import requests
from decouple import config
from . import models as db

# Create your views here.

def ThreadList(response, classId = -1):
    if classId == -1:
        threads = db.Thread.objects.all()
        if threads is not None:
            return render(response, 'ThreadList/index.html', {"threads": threads})
    else:
        threads = db.Thread.objects.filter(class_classid = classId)
        if threads is not None:
            return render(response, 'ThreadList/index.html', {"threads": threads})
    return render(response, "ThreadList/index.html", {})

def Thread(response, thread_id=-1):
    if thread_id != -1:
        thread = db.Thread.objects.filter(threadid = thread_id).first()
        if thread is not None:
            return render(response, 'Thread/index.html', {"thread": thread})

    return render(response, 'Thread/index.html', {"title": "This is a test title"})

def Classes(response, classNum = ''):
    if classNum == '':
       classesL = db.Class.objects.all()
       if classesL is not None:
        return render(response, 'Classes/index.html', {"Classes": classesL}) 
    else:
        classesL = db.Class.objects.filter(classnumber = classNum)
        if classesL is not None:
            return render(response, 'Classes/index.html', {"Classes": classesL}) 
    return render(response, "Classes/index.html", {})