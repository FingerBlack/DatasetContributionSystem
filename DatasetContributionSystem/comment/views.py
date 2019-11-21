from django.shortcuts import render
from dataset.models import dataset
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings

def post(request,datasetname):
    '''
    if request.method == "POST":
        name = request.POST.get("name", '')
        description = request.POST.get('description', '')
        dataset.objects.create(DatasetName = ,
                               Username = ,
                               Description = ,
                               Score = ,
                               Time = )
        return HttpResponseRedirect('/comment/'+name+'/')

    '''

    return render(request,'comment/post.html')

def idex(request,datasetname):
    return render(request,'comment/comment.html')
# Create your views here.
