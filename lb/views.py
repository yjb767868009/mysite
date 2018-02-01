import logging
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

logger = logging.getLogger('lb.views')

def index(request):
    environment_list = Environment.objects.all()
    return render(request, 'lb/index.html', context={'environment_list': environment_list})

@login_required
def account_profile(request):
    messages = []
    if request.method == 'POST':
        request_dic = getattr(request, 'POST')
        form = UserDetailForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.append('successed change!')
    form = UserDetailForm(instance=request.user)
    return render(request, 'account/account_profile.html', context={'form':form,'messages':messages,})

@login_required
def account_detail(request):
    user = request.user
    avatar = user.avatar
    username = user.username
    signature = user.signature
    title = user.title
    department = user.department
    submission_list = Submission.objects.filter(user=user)
    return render(request, 'account/account_detail.html', context={'user':user,
                                                                'avatar':avatar,
                                                                'signature':signature,
                                                                'title':title,
                                                                'department':department,
                                                                'submission_list':submission_list})

def environment_detail(request,pk):
    environment = get_object_or_404(Environment, pk=pk)
    environment.click_increase()
    short_des = environment.short_des
    long_des = environment.long_des
    passing_line = environment.passing_line
    pub_date = environment.pub_date
    join_nb = environment.join_nb
    category_list = environment.category.all()
    submission_list = Submission.objects.filter(environment=environment)
    images = environment.images
    return render(request,'lb/environment_detail.html',context={
                                                                'images':images,
                                                                'environment':environment,
                                                                'short_des':short_des,
                                                                'long_des':long_des,
                                                                'passing_line':passing_line,
                                                                'pub_date':pub_date,
                                                                'join_nb':join_nb,
                                                                'category_list':category_list,
                                                                'submission_list':submission_list})

def submission(request,pk):
    submission = get_object_or_404(Submission, pk=pk)
    description = submission.description
    sub_date = submission.sub_date
    user = submission.user
    environment = submission.environment
    return render(request,'lb/submission.html',context={'submission':submission,
                                                        'description':description,
                                                        'sub_date':sub_date,
                                                        'user':user,
                                                        'environment':environment,})



