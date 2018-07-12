import logging
import re
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

def get_page(request,environment_list,num=5):
    paginator = Paginator(environment_list,num)
    page = request.GET.get('page',1)
    try:
        environment_list = paginator.page(page)
    except(EmptyPage, PageNotAnInteger, InvalidPage):
        environment_list = paginator.page(1)
    return environment_list

def index(request):
    environment_list = Environment.objects.order_by("-click_count")
    environment_list = get_page(request,environment_list,num=6)
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

def environment_detail(request,pk):
    environment = get_object_or_404(Environment, pk=pk)
    environment.click_increase()
    category_list = environment.category.all()
    submission_list = Submission.objects.filter(environment=environment)
    participants_list = environment.participants.all()
    join_nb = 0
    for _ in participants_list:
        join_nb=join_nb+1
    return render(request, 'lb/environment_detail.html', context={'environment':environment,
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

def environment_download(request,pk):
    environment = get_object_or_404(Environment, pk=pk)
    participants_list = environment.participants.all()
    join_nb = 0
    for _ in participants_list:
        join_nb=join_nb+1
    return render(request,'lb/environment_category.html',context={
        'environment':environment,
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


def upload(form, user, environment, sub_name, FILES):

    upload_path = "model/%s/%s/%s/" % (environment.name, user.username, sub_name)
    sub_time = datetime.datetime.now()
    sub_time_str = sub_time.strftime("%Y-%m-%d-%H-%M-%S-%f")
    upload_path = os.path.join(upload_path, sub_time_str)
    upload_path +='/'
    # print('upload_path = '+upload_path)
    if os.path.isdir(upload_path):
        pass
    else:
        os.makedirs(upload_path)
    ckf = FILES.get("checkpoints_file", None)
    with open(os.path.join(upload_path, "checkpoints"), "wb+") as destination:
        for chunk in ckf.chunks():
            destination.write(chunk)
    pgf = FILES.get("test_program_file", None)
    with open(os.path.join(upload_path, "test_program.py"), "wb+") as destination:
        for chunk in pgf.chunks():
            destination.write(chunk)
    file_path = os.path.dirname(os.path.abspath('manage.py'))
    run_path = os.path.join(file_path, upload_path)
    run_path = os.path.join(run_path, "test_program.py")
    run_commend = "python " + run_path + " --path " + upload_path
    print(run_commend)
    os.system(run_commend)

    score_path = os.path.join(upload_path, 'score.txt')
    score_file = open(score_path, 'r')
    score = 0
    try:
        score = score_file.read()
        # print(score)
    finally:
        score_file.close()
    form.add_socre(score)

    if float(score) > environment.passing_line:
        environment.solved = 'solved'
    form.add_time(sub_time)

    form.save()


@login_required
def submit(request,pk):
    environment = get_object_or_404(Environment, pk=pk)
    messages = []
    if request.method == 'POST':

        form = SubmissionForm(environment,request.user,request.POST,request.FILES)
        form.owner = request.user
        form.environment = environment
        if form.is_valid():
            sub_name = request.POST.get('name','')

            if ' ' in sub_name:
                messages.append('Please input name without spaces')
                return render(request, 'lb/submit.html', context={'form':form,'error_messages': messages,'environment': environment})

            upload(form,request.user,environment,sub_name,request.FILES)

            messages.append('successed submit!')
            return render(request, 'lb/environment_detail.html', context={'messages':messages,
                                                                 'environment': environment})
        else:
            messages.append('error1')
    else:
        form = SubmissionForm(environment,request)
    return render(request, 'lb/submit.html', context={
        'form':form,
        'messages':messages,
        'environment':environment})
