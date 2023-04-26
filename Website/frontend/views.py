import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import requests
from decouple import config
from . import models as db
from datetime import datetime
from .MLModel.input_matching import query_model
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.conf.urls.static import static
# Create your views here.

@csrf_exempt
def ThreadList(request, classId = -1, filter = ''):
    if request.method == "DELETE":
        data = json.loads(request.body)
        db.Reply.objects.filter(thread_threadid = data["threadid"]).delete()
        db.Thread.objects.filter(threadid=data["threadid"]).delete()
        return JsonResponse(classId, safe=False)
    else:
        threads = []
        if classId == -1:
            classId = request.session["class_id"]
        else:
            request.session["class_id"] = classId
            return redirect("ThreadList")
        
        threads = db.Thread.objects.filter(class_classid = classId).order_by("-creationdate")

        if filter:
            threads = threads.filter(threadcontent__icontains=filter)

        class_name = db.Class.objects.filter(classid = classId).first().classname

        if threads is not None:
            return render(request, 'ThreadList/index.html', {"class_name": class_name, "threads": threads})         



@csrf_exempt
def Thread(request, thread_id=-1, Delete = ''):
    if request.method == "POST":
        # Create Thread

        data = json.loads(request.body)
        if data["repid"] == -1:
            print(data["description"])
            threadObj = db.Thread.objects.filter(threadid=thread_id).first()
            classObj = db.Class.objects.filter(classid=24313).first()
            studentObj = db.Student.objects.filter(netid="abc123000").first()
            newReply = db.Reply.objects.create(thread_threadid = threadObj,
                                            creationdate = datetime.now(),
                                            content = data["description"],
                                            student_netid = studentObj)
        else:
            print(data["description"])
            threadObj = db.Thread.objects.filter(threadid=thread_id).first()
            classObj = db.Class.objects.filter(classid=24313).first()
            studentObj = db.Student.objects.filter(netid="abc123000").first()
            newReply = db.Reply.objects.create(thread_threadid = threadObj,
                                            creationdate = datetime.now(),
                                            content = data["description"],
                                            student_netid = studentObj,
                                            parent_replyid = data["repid"])
        return JsonResponse(thread_id, safe=False)
    elif request.method == "DELETE":
        data = json.loads(request.body)
        db.Reply.objects.filter(parent_replyid = data["repid"]).delete()
        db.Reply.objects.filter(replyid = data["repid"]).delete()
        return JsonResponse(thread_id, safe=False)
    else:
        if thread_id != -1:
            thread = db.Thread.objects.filter(threadid = thread_id).first()
            if thread is not None:
                thread.replies = db.Reply.objects.filter(thread_threadid=thread_id).filter(parent_replyid__isnull =True).order_by("-creationdate")
                for i in thread.replies:
                    repid = i.replyid
                    i.replies = db.Reply.objects.filter(thread_threadid=thread_id).filter(parent_replyid = repid).order_by("creationdate")
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
        
        net_id = request.session["net_id"]
        class_id = request.session["class_id"]

        data = json.loads(request.body)
        print(data["title"])
        
        classObj = db.Class.objects.filter(classid=class_id).first()
        studentObj = db.Student.objects.filter(netid=net_id).first()

        newThread = db.Thread.objects.create(threadtitle=data["title"], 
                                             threadcontent=data["description"],
                                             class_classid=classObj,
                                             creationdate=datetime.now(),
                                             student_netid=studentObj)
        
        __QueryModel(request, data["description"], newThread)
        
        return JsonResponse(newThread.threadid, safe=False)
    return render(request, "CreateThread/index.html", {})


def __QueryModel(request, query, thread):
    class_id = request.session["class_id"]

    if class_id is None:
        return

    result = query_model(class_id, query)

    botStudentObj = db.Student.objects.filter(netid = "bot000001").first()
    
    thread_list, doc_list = result

    thread_list = [*set(thread_list)]
    doc_list = [*set(doc_list)]

    print("Thread_List", thread_list)
    print("Doc", doc_list)

    reply = ""

    if thread_list:
        if len(reply) > 1:
            reply += "These threads may help you: " 
        else:
            reply += "This thread may help you: " 
        for thr in thread_list:
            # Temporary. Will replace with hyperlinks.
            reply += "\n\t" + str(thr)

    if doc_list:
        if reply:
            reply += "\n"

        if len(doc_list) > 1:
            reply += "These documents may help you: " 
        else:
            reply += "This document may help you: " 
        for doc in doc_list:
            # Temporary. Will replace with hyperlinks.
            reply += "\n\t" + str(doc)
            

    if reply:
        db.Reply.objects.create(
            thread_threadid = thread,
            creationdate=datetime.now(),
            content=reply,
            student_netid = botStudentObj
        )

def LoginUser(request, net_id):
    student = db.Student.objects.filter(netid = net_id).first()
    # For testing at the moment, just grab the first class they're enrolled in
    enrollment = db.Enrollment.objects.filter(student_netid = student).first()
    
    # set session information
    request.session.clear()
    request.session["net_id"] = net_id
    request.session["class_id"] = enrollment.class_classid.classid

    return redirect('Classes')

@csrf_exempt
def uploadFile(request,classId = -1):
    if request.method == "POST":
        # Create Thread
        #data = json.loads(request.body)
        
        #uploaded_File = request.FILES.getlist["FileDoc"]
        for f in  request.FILES.getlist("FileDoc"):
            sizeF = f.content_type + ''
            if len(sizeF) >= 45:
                sizeF = sizeF[0:12] + sizeF[46:71]
            storageurl = settings.MEDIA_URL +  '/' + str(classId) + '/'
            storagePath = settings.MEDIA_ROOT +  '/' + str(classId) + '/'
            fpath = settings.MEDIA_ROOT +  '/' + str(classId) + '/' + f.name
            fileSave = FileSystemStorage(location=storagePath,base_url=storageurl)
            fileSave.save(f.name,f)
            classObj = db.Class.objects.filter(classid=classId).first()
            newFile = db.File.objects.create(filename=f.name,
                                            filetype=sizeF,
                                            filecontent=fpath,
                                            class_classid=classObj)
        return render(request, "FileUpload/index.html", {})
        
    return render(request, "FileUpload/index.html", {})
