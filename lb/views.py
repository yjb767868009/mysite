import logging
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from .models import *
import os
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
    submission_list = Submission.objects.filter(owner=subscriber)
    environment_list = Environment.objects.filter(participants=subscriber)
    return render(request, 'account/account_detail.html', context={'subscriber':subscriber,
                                                                'submission_list':submission_list,
                                                                'environment_list':environment_list})

def environment(request,pk):
    environment = get_object_or_404(Environment, pk=pk)
    environment.click_increase()
    category_list = environment.category.all()
    submission_list = Submission.objects.filter(environment=environment)
    participants_list = environment.participants.all()
    join_nb = 0
    for _ in participants_list:
        join_nb=join_nb+1
    return render(request,'lb/environment.html',context={'environment':environment,
                                                                'join_nb':join_nb,
                                                                'category_list':category_list,
                                                                'submission_list':submission_list,
                                                                'participants_list':participants_list})

def environment_leaderboard(request,pk):
    environment = get_object_or_404(Environment, pk=pk)
    submission_list = Submission.objects.filter(environment=environment)
    participants_list = environment.participants.all()
    join_nb = 0
    for _ in participants_list:
        join_nb=join_nb+1
    return render(request,'lb/environment_leaderboard.html',context={
        'environment':environment,
        'submission_list':submission_list,
        'join_nb': join_nb
    })

def environment_discussion(request,pk):
    environment = get_object_or_404(Environment, pk=pk)
    participants_list = environment.participants.all()
    join_nb = 0
    for _ in participants_list:
        join_nb=join_nb+1
    return render(request,'lb/environment_discussion.html',context={
        'environment':environment,
        'join_nb': join_nb
    })

def environment_category(request,pk):
    environment = get_object_or_404(Environment, pk=pk)
    category_list = environment.category.all()
    participants_list = environment.participants.all()
    join_nb = 0
    for _ in participants_list:
        join_nb=join_nb+1
    return render(request,'lb/environment_category.html',context={
        'environment':environment,
        'category_list':category_list,
        'join_nb': join_nb
    })

def submission(request,pk):
    submission = get_object_or_404(Submission, pk=pk)
    environment = submission.environment
    return render(request,'lb/submission.html',context={'submission':submission,
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
        error_msg = 'Please submit a search term.'
        return render(request,'lb/search.html',context={'error_msg':error_msg})
    environment_list = Environment.objects.filter(name__contains = q)
    environment_list = get_page(request,environment_list)
    return render(request,'lb/search.html',context={'error_msg':error_msg,'environment_list':environment_list})

@login_required
def submit(request,pk):
    environment = get_object_or_404(Environment, pk=pk)
    messages = []
    if request.method == 'POST':
        form = SubmissionForm(environment,request.user,request.POST,request.FILES)
        form.owner = request.user
        form.environment = environment
        if form.is_valid():
            form.save()
            sub_name = request.POST.get('name','')
            upload_path = "upload/%s/%s/" % (environment.name, sub_name)
            if os.path.isdir(upload_path):
                pass
            else:
                os.makedirs(upload_path)
            ckf = request.FILES.get("checkpoints_file",None)
            with open(os.path.join(upload_path,"checkpoints"), "wb+") as destination:
                for chunk in ckf.chunks():
                    destination.write(chunk)
            pgf = request.FILES.get("test_program_file", None)
            with open(os.path.join(upload_path,"test_program.py"), "wb+") as destination:
                for chunk in pgf.chunks():
                    destination.write(chunk)
            # upload_checkpoints(request.FILES['checkpoints_file'])
            # upload_program(request.FILES['test_program_file'])
            messages.append('successed submit!')
            return render(request,'lb/environment.html',context={'messages':messages,
                                                                 'environment': environment})
        else:
            messages.append('error1')
    else:
        form = SubmissionForm(environment,request)
    return render(request, 'lb/submit.html', context={
        'form':form,
        'messages':messages,
        'environment':environment})

def upload_checkpoints(f):
    destination = open(os.path.join("media"))



def upload_program(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)