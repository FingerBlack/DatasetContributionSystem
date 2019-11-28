from django.shortcuts import render
from .models import comment
from .models import likelike
from dataset.models import dataset
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
import os, zipfile, shutil, uuid, json, datetime
from django.views.decorators.cache import cache_page

@login_required
def post(request,datasetname):

    if request.method == "POST":
        description = request.POST.get('description', '')
        score = request.POST.get('score')
        #print(score)
        #print(request.user.username)
        comment.objects.create(DatasetName = dataset.objects.get(name=datasetname),
                               Username = request.user,
                               Description = description,
                               Score = int(score))
        return HttpResponseRedirect('/dataset/'+datasetname+'/comment/')
    return render(request,'comment/post.html')

def idex(request,datasetname):
    data = dataset.objects.get(name = datasetname)

    cc = likelike.objects.filter(DatasetName=data)
    countt = cc.count()

    try:
        likelike.objects.get(DatasetName=data,Username=request.user)
        i = -1
    except:
        i = 1

    return render(request, 'comment/comment.html',{'comment': comment.objects.filter(DatasetName=data), 'check': data, 'i': i, 'countt': countt})

@login_required
def delete(request,datasetname):
    ret = {}
    if request.method == "POST":

        id = request.POST.get('id','')
        dh = comment.objects.get(id=id)
        return HttpResponse(dh.delete())
    ret['status'] = 'ok'
    return HttpResponse(json.dumps(ret))

@login_required
def like(request,datasetname):

    data = dataset.objects.get(name=datasetname)
    ret = {}
    print(12212)
    if request.method == "POST":
        dn = request.POST.get('name','')
        cc = likelike.objects.filter(DatasetName=data,Username=request.user)
        print(2222)

        if cc.count() == 0:
            print(1)
            likelike.objects.create(DatasetName=data,Username=request.user)
        else:
            cc.delete()
    return render(request, 'comment/comment.html',{'comment': comment.objects.filter(DatasetName=data), 'check': comment.objects.filter(DatasetName=data).first()})
# Create your views here.
