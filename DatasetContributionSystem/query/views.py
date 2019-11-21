from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
import os
from dataset.models import dataset
# Create your views here.
def index(request):
    return render(request, 'querypage/query.html', {'dataset': dataset.objects.all()})

def search(request):
    if  request.method == "GET":
        x = request.GET.get("Datasetname")
        y = request.GET.get("Taskname")
        name_list = dataset.objects.filter(name__contains=x)
        if not x and not y:
            return render(request, 'querypage/query.html')
        return render(request, 'querypage/result.html', {'dataset': name_list})