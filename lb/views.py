import logging
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

logger = logging.getLogger('lb.views')

def global_setting(request):
    return {'SITE_NAME':settings.SITE_NAME,'STIE_DESCP':settings.SITE_DESCP,'SITE_KEYWORDS':settings.SITE_KEYWORDS}

def get_page(request,environment_list):
    paginator = Paginator(environment_list,5)
    page = request.GET.get('page',1)
    try:
        environment_list = paginator.page(page)
    except(EmptyPage, PageNotAnInteger, InvalidPage):
        environment_list = paginator.page(1)
    return environment_list

def index(request):
    environment_list = Environment.objects.order_by("-click_count")
    environment_list = get_page(request,environment_list)
    return render(request, 'lb/index.html', context={'environment_list': environment_list})

def environment_list(request):
    environment_list = Environment.objects.order_by("-pub_date")
    environment_list = get_page(request,environment_list)
    return render(request, 'lb/environment_list.html', context={'environment_list': environment_list})

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

def account_detail(request):
    user = request.user
    avatar = user.avatar
    username = user.username
    signature = user.signature
    title = user.title
    department = user.department
    submission_list = Submission.objects.filter(user=user)
    environment_list = Environment.objects.filter(user=user)
    return render(request, 'account/account_detail.html', context={'user':user,
                                                                'avatar':avatar,
                                                                'signature':signature,
                                                                'title':title,
                                                                'department':department,
                                                                'submission_list':submission_list,
                                                                'environment_list':environment_list})

def environment(request,pk):
    environment = get_object_or_404(Environment, pk=pk)
    environment.click_increase()
    short_des = environment.short_des
    long_des = environment.long_des
    passing_line = environment.passing_line
    pub_date = environment.pub_date
    join_nb = environment.join_nb
    category_list = environment.category.all()
    submission_list = Submission.objects.filter(environment=environment)
    user_list = environment.user.all()
    images = environment.images
    solved = environment.solved
    return render(request,'lb/environment.html',context={'environment':environment,
                                                                'images':images,
                                                                'short_des':short_des,
                                                                'long_des':long_des,
                                                                'passing_line':passing_line,
                                                                'pub_date':pub_date,
                                                                'join_nb':join_nb,
                                                                'solved':solved,
                                                                'category_list':category_list,
                                                                'submission_list':submission_list,
                                                                'user_list':user_list})

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

def search(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = ''
        return render(request,'blog/search.html',context={'error_msg':error_msg})
    environment_list = Environment.objects.filter(title__contains = q)
    environment_list = get_page(request,environment)
    return render(request,'blog/search.html',context={'error_msg':error_msg,'environment_list':environment_list})

@login_required
def submit(request):
    messages = []
    if request.method == 'POST':
        request_dic = getattr(request, 'POST')
        form = SubmissionForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.append('successed submit!')
    form = SubmissionForm()
    return render(request, 'lb/submit.html', context={'form':form,'messages':messages,})
