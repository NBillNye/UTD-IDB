import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
from decouple import config
from . import models as db
from datetime import datetime
from .MLModel.text_extractor_docx import ask_bert
import os

# Create your views here.

def ThreadList(request, classId = -1):
    if classId == -1:
        threads = db.Thread.objects.all().order_by("-creationdate")
        if threads is not None:
            return render(request, 'ThreadList/index.html', {"threads": threads})
    else:
        threads = db.Thread.objects.filter(class_classid = classId)
        if threads is not None:
            return render(request, 'ThreadList/index.html', {"threads": threads})
    return render(request, "ThreadList/index.html", {})
@csrf_exempt
def Thread(request, thread_id=-1):
    if request.method == "POST":
        # Create Thread

        data = json.loads(request.body)
        print(data["description"])
        threadObj = db.Thread.objects.filter(threadid=thread_id).first()
        classObj = db.Class.objects.filter(classid=24313).first()
        studentObj = db.Student.objects.filter(netid="abc123000").first()
        newReply = db.Reply.objects.create(thread_threadid = threadObj,
                                           creationdate = datetime.now(),
                                           content = data["description"],
                                           student_netid = studentObj)
        return JsonResponse(thread_id, safe=False)
    else:
        if thread_id != -1:
            thread = db.Thread.objects.filter(threadid = thread_id).first()
            if thread is not None:
                thread.replies = db.Reply.objects.filter(thread_threadid=thread_id).order_by("-creationdate")

                return render(request, 'Thread/index.html', {"thread": thread})

    return render(request, 'Thread/index.html', {})

def Classes(request, classNum = ''):
    if classNum == '':
       classesL = db.Class.objects.all()
       if classesL is not None:
        return render(request, 'Classes/index.html', {"Classes": classesL}) 
    else:
        classesL = db.Class.objects.filter(classnumber = classNum)
        if classesL is not None:
            return render(request, 'Classes/index.html', {"Classes": classesL}) 
    return render(request, "Classes/index.html", {})

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
        
        __AskBert(data["description"], newThread)
        
        return JsonResponse(newThread.threadid, safe=False)
    return render(request, "CreateThread/index.html", {})


def __AskBert(query, thread):
    result = ask_bert('Syllabus-3377-converted.docx', query)

    botStudentObj = db.Student.objects.filter(netid = "bot000001").first()
    
    print('\nRESULT: ', result, '\n')

    if result['score'] >= 0.5:
        db.Reply.objects.create(
            thread_threadid = thread,
            creationdate=datetime.now(),
            content=result["answer"],
            student_netid = botStudentObj
        )