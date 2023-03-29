from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def GetThreadList(request, user_id):
    if(request.method == "POST"):
        
        threads = [
            {"user_id": user_id, "Name": "Thread Name", "Author": "John Smith", "Date": "01/02/2023", "Description": "this is a test description"},
            {"user_id": user_id, "Name": "Thread Name 2", "Author": "John Smith", "Date": "01/01/2023", "Description": "this is a test description"},
            {"user_id": user_id, "Name": "Thread Name 3", "Author": "Ryan Talbot", "Date": "01/01/2023", "Description": "this is a test description"},
            ]

        # Get Thread data from database based off of UserId

        return JsonResponse(threads, safe=False)
    return HttpResponseBadRequest()
    