from django.shortcuts import render
from .models import comment
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
    return render(request, 'comment/comment.html',{'comment': comment.objects.filter(DatasetName=data), 'check': comment.objects.filter(DatasetName=data).first()})

def delete(request,datasetname):
    ret = {}
    if request.method == "POST":

        id = request.POST.get('id','')
        dh = comment.objects.get(id=id)
        return HttpResponse(dh.delete())
    ret['status'] = 'ok'
    return HttpResponse(json.dumps(ret))

def like(request,datasetname):
    #print(11111)
    ret = {}
    if request.method == "POST":
        dn = request.POST.get('name','')
        #print(dn)
        dd = comment.objects.filter(DatasetName=dataset.objects.get(name = dn))

        todo = dd.values("Like")
        #print(todo)
        for item in dd:
            item.Like = item.Like+1
            item.save()
        dd = comment.objects.filter(DatasetName=dataset.objects.get(name=dn))

        todo = dd.values("Like")
        #print(todo)
    data = dataset.objects.get(name=datasetname)
    return render(request, 'comment/comment.html',{'comment': comment.objects.filter(DatasetName=data), 'check': comment.objects.filter(DatasetName=data).first()})
# Create your views here.
