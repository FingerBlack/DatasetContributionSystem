from django.shortcuts import render
from .models import dataset
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.conf import settings
import os

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
        filename = myfile.name
        filepath = os.path.join("./"+settings.MEDIA_ROOT, filename)
        f = open(filepath,'wb+')
        for chunk in myfile.chunks():
            f.write(chunk)
        f.close()
    return render(request, 'dataset/upload.html')

def show(request, datasetname):
    return render(request, 'dataset/show.html', {'dataset': dataset.objects.get(name=datasetname)})
<<<<<<< HEAD

def download(request, datasetname):
    return render(request, 'dataset/download.html', {'dataset': dataset.objects.get(name=datasetname)})
=======
>>>>>>> 82557c321e4ae0af6e431faada45cf89d2bac830
