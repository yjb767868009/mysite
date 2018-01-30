import logging
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from .models import *
from .forms import UserDetailForm
from django.contrib.auth.decorators import login_required


def index(request):
    envir_list = Environment.objects.all()
    return render(request, 'lb/index.html', context={'envir_list': envir_list})

@login_required
def account_profile(request):
    messages = []
    if request.method == 'POST':
        #request_dic = getattr(request, 'POST')
        #print(request_dic)
        #print(request.FILES)
        form = UserDetailForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.append('successed change!')
    form = UserDetailForm(instance=request.user)
    return render(request, 'account/user_detail.html', context={'form':form,'messages':messages,})

def environment_detail(request,pk):
    environment = get_object_or_404(Environment, pk=pk)
    environment.click_increase()
    description = environment.long_des
    passing_line = environment.passing_line
    pub_date = envir.pubdate
    return render(request,'lb/environment_detail.html',context={'environment'=environment,'description'=description,'passing_line'=passing_line,'pubdate'=pubdate})

def submission(request):
    return HttpResponse("This is submission")



