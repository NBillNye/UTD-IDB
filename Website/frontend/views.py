from django.shortcuts import render

# Create your views here.

def ThreadList(response):
    return render(response, "ThreadList/index.html", {})