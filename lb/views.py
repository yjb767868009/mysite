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

def account_detail(request,username):
    subscriber = get_object_or_404(User,username=username)
    username = subscriber.username
    signature = subscriber.signature
    title = subscriber.title
    department = subscriber.department
    submission_list = Submission.objects.filter(owner=subscriber)
    environment_list = Environment.objects.filter(participants=subscriber)
    return render(request, 'account/account_detail.html', context={'subscriber':subscriber,
                                                                'username':username,
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
    category_list = environment.category.all()
    submission_list = Submission.objects.filter(environment=environment)
    participants_list = environment.participants.all()
    join_nb = 0
    for participant in participants_list:
        join_nb=join_nb+1
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
                                                                'participants_list':participants_list})

def environment_leaderboard(request,pk):
    environment = get_object_or_404(Environment, pk=pk)
    submission_list = Submission.objects.filter(environment=environment)
    return render(request,'lb/environment_leaderboard.html',context={'environment':environment,
                                                                'submission_list':submission_list})

def environment_discussion(request,pk):
    environment = get_object_or_404(Environment, pk=pk)
    return render(request,'lb/environment_discussion.html',context={'environment':environment})

def environment_category(request,pk):
    environment = get_object_or_404(Environment, pk=pk)
    category_list = environment.category.all()
    return render(request,'lb/environment_category.html',context={'environment':environment,
                                                                'category_list':category_list})

def submission(request,pk):
    submission = get_object_or_404(Submission, pk=pk)
    description = submission.description
    sub_date = submission.sub_date
    owner = submission.owner
    environment = submission.environment
    return render(request,'lb/submission.html',context={'submission':submission,
                                                        'description':description,
                                                        'sub_date':sub_date,
                                                        'owner':owner,
                                                        'environment':environment,})

def submission_bestrwards(request,pk):
    submission = get_object_or_404(Submission, pk=pk)
    environment = submission.environment
    owner = submission.owner
    return render(request,'lb/submission_bestrwards.html',context={'submission':submission, 
                                                       'owner':owner,
                                                        'environment':environment,})

def submission_episodes(request,pk):
    submission = get_object_or_404(Submission, pk=pk)
    environment = submission.environment
    owner = submission.owner
    return render(request,'lb/submission_episodes.html',context={'submission':submission,
                                                        'owner':owner,
                                                        'environment':environment,})

def submission_discussion(request,pk):
    submission = get_object_or_404(Submission, pk=pk)
    environment = submission.environment
    owner = submission.owner
    return render(request,'lb/submission_discussion.html',context={'submission':submission,
                                                        'owner':owner,
                                                        'environment':environment,})


def search(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = ''
        return render(request,'lb/search.html',context={'error_msg':error_msg})
    environment_list = Environment.objects.filter(title__contains = q)
    environment_list = get_page(request,environment)
    return render(request,'lb/search.html',context={'error_msg':error_msg,'environment_list':environment_list})

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
