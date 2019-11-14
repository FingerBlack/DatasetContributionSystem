from django.shortcuts import render
from .models import comment
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

from django.conf import settings
import os

def idex(request,datasetname):
    return render(request,'comment/comment.html',{'dataset':datasetname})

@login_required
def post(request,datasetname):
    if request.method == "POST":
        name = request.POST.get("name", '')
        score = float(request.POST.get("score", ''))
        description = request.POST.get('description', '')
        comment.objects.create(Datasetname=name,
                               Score=score,
                               Descriptin = description,
                               Username=request.user.username)
        return HttpResponseRedirect('/comment/'+name+'/')
    return render(request,'comment/post.html')

# Create your views here.
