from django.shortcuts import render
from .models import dataset
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
import os, zipfile

# Create your views here.
def index(request):
    return render(request, 'dataset/dataset.html', {'dataset': dataset.objects.all()})

@login_required
def create(request):
    if request.method == "POST":
        name = request.POST.get("name", '')
        price = float(request.POST.get("price", ''))
        datatype = request.POST.get("datatype", '')
        description = request.POST.get('description', '')
        dataset.objects.create(name=name, 
                               price=price, 
                               dataType=datatype, 
                               pv=0, 
                               description = description,
                               owner=request.user.username)
        return HttpResponseRedirect('/dataset/'+name+'/')
    return render(request, 'dataset/create.html')

@login_required
def upload_view(request, datasetname):
    if request.method == 'POST':
        myfile = request.FILES.get('file')
        zf = zipfile.ZipFile(myfile)
        filename = myfile.name
        filepath = os.path.join("./"+settings.MEDIA_ROOT + "/tmp/", filename)
        zf.extractall(path=filepath)
        return HttpResponse('success')
    return render(request, 'dataset/upload.html', {'datasetname':datasetname})

def show(request, datasetname):
    return render(request, 'dataset/show.html', {'dataset': dataset.objects.get(name=datasetname)})

def download(request, datasetname):
    return render(request, 'dataset/download.html', {'dataset': dataset.objects.get(name=datasetname)})
