from django.shortcuts import render
from .models import comment
from dataset.models import dataset
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
@login_required
def post(request,datasetname):

    if request.method == "POST":
        description = request.POST.get('description', '')
        print(request.user.username)
        comment.objects.create(DatasetName = dataset.objects.get(name=datasetname),
                               Username = request.user,
                               Description = description,
                               Score = 70)
        return HttpResponseRedirect('/comment/'+datasetname+'/')
    return render(request,'comment/post.html')

def idex(request,datasetname):
    return render(request,'comment/comment.html', {'comment': comment.objects.all()})
# Create your views here.
