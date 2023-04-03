from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def GetUserInformation(request, user_id):
    if request.method == "POST":
        obj = {"user_id": user_id}

        # Get user data from database

        return JsonResponse(obj)
    return HttpResponseBadRequest()