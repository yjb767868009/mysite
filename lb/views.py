from django.http import HttpResponse
from django.shortcuts import render
from .models import Environment,User

def index(request):
    best_envir_list = Environment.objects.order_by('-join_nb')[:5]
    output = ', '.join([q.name for q in best_envir_list])
    return HttpResponse(output)

def user(request):
    return HttpResponse("This is user.")

def environment(request):
    return HttpResponse("This is environmnet.")

def submission(request):
    return HttpResponse("This is submission")



