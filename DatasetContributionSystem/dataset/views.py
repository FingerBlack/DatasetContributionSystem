from django.shortcuts import render
from .models import dataset
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
import os, zipfile, shutil, uuid

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
    data = dataset.objects.get(name = datasetname)
    if request.method == 'POST':
        myfile = request.FILES.get('file')
        zf = zipfile.ZipFile(myfile)
        filename = myfile.name
        filepath = os.path.join("./"+settings.MEDIA_ROOT + "/tmp/", filename)
        zf.extractall(path=filepath)
        pic_list = os.listdir(filepath+'/'+os.listdir(filepath)[0]+'/')

        src = filepath+'/'+os.listdir(filepath)[0]+'/'
        dest = os.path.join("./"+settings.MEDIA_ROOT, 'dataset', datasetname)

        if os.path.exists(dest) == False:
            os.mkdir(dest)

        dataset_len = 0
        for item in pic_list:
            tmp = item.split('.')
            pic_pre = '.'.join(tmp[:-1])
            if tmp[-1] == 'jpg' and os.path.exists(src + '/' + pic_pre + '.txt'):
               dataset_len += 1
               randomname = str(uuid.uuid4())
               shutil.move(src+'/'+ pic_pre + '.txt', dest + '/'+ randomname + '.txt')
               shutil.move(src+'/'+ pic_pre + '.jpg', dest + '/'+ randomname + '.jpg')
        
        data.size += dataset_len
        print(data.size, dataset_len)
        if os.path.exists(filepath) == True:
            shutil.rmtree(filepath)
        data.save()
        return HttpResponse('success')
    
    return render(request, 'dataset/upload.html', {'datasetname':datasetname})

def show(request, datasetname):
    return render(request, 'dataset/show.html', {'dataset': dataset.objects.get(name=datasetname)})

def download(request, datasetname):
    return render(request, 'dataset/download.html', {'dataset': dataset.objects.get(name=datasetname)})
