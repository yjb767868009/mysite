import logging
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from .models import *
from .forms import UserDetailForm
from django.contrib.auth.decorators import login_required


def index(request):
    environment_list = Environment.objects.all()
    return render(request, 'lb/index.html', context={'environment_list': environment_list})

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
    short_des = environment.short_des
    long_des = environment.long_des
    passing_line = environment.passing_line
    pub_date = environment.pub_date
    join_nb = environment.join_nb
    category_list = enviironment.category.all()
    submission_list = environment.submission.all()
    return render(request,'lb/environment_detail.html',context={'environment':environment,
                                                                'short_des':short_des,
                                                                'long_des':long_des,
                                                                'passing_line':passing_line,
                                                                'pub_date':pub_date,
                                                                'join_nb':join_nb,
                                                                'category_list':category_list,
                                                                'submission_list':submission_list})

def submission(request,pk):
    submission = get_object_or_404(Environment, pk=pk)
    description = submission.des
    sub_date = submission.sub_date
    user = submission.user
    environment = submission.environment
    return render(request,'lb/submission.html',context={'description':description,
                                                        'sub_date':sub_date,
                                                        'user':user,
                                                        'environment':environment,})



