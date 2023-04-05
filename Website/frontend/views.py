import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
from decouple import config
from . import models as db
from datetime import datetime

# Create your views here.

def ThreadList(request):
    threads = db.Thread.objects.all().order_by("-creationdate")
    if threads is not None:
        return render(request, 'ThreadList/index.html', {"threads": threads})
    return render(request, "ThreadList/index.html", {})

def Thread(request, thread_id=-1):
    if thread_id != -1:
        thread = db.Thread.objects.filter(threadid = thread_id).first()
        if thread is not None:
            thread.replies = db.Reply.objects.filter(thread_threadid=thread_id).order_by("-creationdate")

            return render(request, 'Thread/index.html', {"thread": thread})

    return render(request, 'Thread/index.html', {"title": "This is a test title"})

@csrf_exempt
def CreateThread(request):
    if request.method == "POST":
        # Create Thread

        data = json.loads(request.body)
        print(data["title"])
        
        classObj = db.Class.objects.filter(classid=24313).first()
        studentObj = db.Student.objects.filter(netid="abc123000").first()

        newThread = db.Thread.objects.create(threadtitle=data["title"], 
                                             threadcontent=data["description"],
                                             class_classid=classObj,
                                             creationdate=datetime.now(),
                                             student_netid=studentObj)
        
        
        return JsonResponse(newThread.threadid, safe=False)
    return render(request, "CreateThread/index.html", {})