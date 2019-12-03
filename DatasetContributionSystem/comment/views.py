from django.shortcuts import render
from .models import comment, star
from dataset.models import dataset
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
import os, zipfile, shutil, uuid, json, datetime
from django.views.decorators.cache import cache_page


@login_required
def post(request, datasetname):
    if request.method == "POST":
        description = request.POST.get('description', '')
        score = request.POST.get('score')
        # print(score)
        # print(request.user.username)
        if len(description)>1000:
            return render(request, 'failure.html', {'title': '提交评论失败（字数限制）'})
        else:
            comment.objects.create(DatasetName=dataset.objects.get(name=datasetname),
                                   Username=request.user,
                                   Description=description,
                                   Score=int(score))
            return HttpResponseRedirect('/dataset/' + datasetname + '/comment/')
    return render(request, 'comment/post.html')


def idex(request, datasetname):
    data = dataset.objects.get(name=datasetname)
    dh = comment.objects.filter(DatasetName=data)
    avg_score = 0
    if dh.count() < 2:
        avg_score = -1
    else:
        for item in dh:
            avg_score = item.Score + avg_score
        avg_score = avg_score / dh.count()
        avg_score = int(avg_score)
    print(avg_score)
    return render(request, 'comment/comment.html',
                  {'comment': comment.objects.filter(DatasetName=data).order_by('-id'), 'avg_score': avg_score})


@login_required
def delete(request, datasetname):
    ret = {}
    if request.method == "POST":
        id = request.POST.get('id', '')
        dh = comment.objects.get(id=id)
        return HttpResponse(dh.delete())
    ret['status'] = 'ok'
    return HttpResponse(json.dumps(ret))

@login_required
def star_views(request, datasetname):
    ret = {}
    try:
        data = dataset.objects.get(name=datasetname)
    except:
        ret["message"] = "no such dataset"
        return HttpResponse(json.dumps(ret))
    if star.objects.filter(DatasetName=data, Username=request.user).exists():
        ret["message"] = "remove star ok"
        star.objects.filter(DatasetName=data, Username=request.user).delete()
        data.star -= 1
        data.save()
    else:
        ret["message"] = "add star ok"
        star.objects.create(DatasetName=data, Username=request.user)
        data.star += 1
        data.save()
    return HttpResponse(json.dumps(ret))

@login_required
def change(request, datasetname, commentid):

    if request.method == "POST":
        description = request.POST.get('description', '')
        score = request.POST.get('score', '')
        try:
            comment_tmp = comment.objects.get(id=commentid, Username=request.user)
        except:
            return render(request, 'failure.html', {'title': '不存在此条评论'})
        comment_tmp.Description = description
        comment_tmp.Score = score
        comment_tmp.save()
        return render(request, 'success.html', {'title': '修改评论成功'})
    return render(request, 'comment/ch.html',{'commentchange': comment.objects.get(id=commentid)})

# Create your views here.

