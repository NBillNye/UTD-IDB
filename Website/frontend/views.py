from django.shortcuts import render
import requests
from decouple import config

# Create your views here.

def ThreadList(response):
    print("REQUEST >>>> ", config("API_URL") + "threads/GetThreadList/1/")
    threads = requests.post(config("API_URL") + "threads/GetThreadList/1/")
    print("RESPONSE >>>> ", threads)
    if threads is not None:
        threads_data = threads.json()
        print("threads_data >>>> ", threads_data)
        return render(response, "ThreadList/index.html", {"threads": threads_data})
    return render(response, "ThreadList/index.html", {})
        