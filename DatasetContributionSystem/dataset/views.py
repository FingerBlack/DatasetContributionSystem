from django.shortcuts import render
from .models import dataset
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
import os, zipfile, shutil, uuid, json

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
                               description=description,
                               owner=request.user.username)
        return HttpResponseRedirect('/dataset/'+name+'/')
    return render(request, 'dataset/create.html')

class Upload():
    #define the relation between function and type
    def image_recognition(self):
        ret = {}
        zf = None
        try:
            zf = zipfile.ZipFile(self.file)
            zf.testzip()
        except:
            ret['status'] = 'error'
            ret['message'] = 'bad zip file'
            return ret
        dir_dest = os.path.join('.' + settings.MEDIA_ROOT, 'dataset', self.dataset.name)
        #check whether the dataset is empty
        if os.path.exists(dir_dest) == False:
            os.mkdir(dir_dest)
        ret['status'] = 'ok'
        ret['acceptFileList'] = []
        for item in zf.infolist():
            fn_jpg = item.filename.split('.')
            if fn_jpg[-1] != 'jpg':
                #ignore the file
                continue
            fn_txt = fn_jpg.copy()
            fn_txt[-1] = 'txt'
            if '.'.join(fn_txt) not in zf.namelist():
                #ignore the file which has no tag
                continue
            ret['acceptFileList'].append('.'.join(fn_jpg))
            targetName = str(uuid.uuid4())
            with open(os.path.join(dir_dest, targetName + '.jpg'), 'wb') as f:
                f.write(zf.read('.'.join(fn_jpg)))
            with open(os.path.join(dir_dest, targetName + '.txt'), 'wb') as f:
                f.write(zf.read('.'.join(fn_txt)))
            self.dataset.size += 1
        self.dataset.save()
        return ret
    type_to_func = {2: image_recognition, 1: image_recognition}
    def __init__(self, file, dataset):
        self.file = file
        self.dataset = dataset
    def handle(self):
        return HttpResponse(json.dumps(self.type_to_func[self.dataset.dataType](self)))

@login_required
def upload_view(request, datasetname):
    data = dataset.objects.get(name = datasetname)
    if data == None:
        return render(request, 'failure.html', {'title': '所选数据集不存在'})
    if request.method == 'POST':
        myfile = request.FILES.get('file')
        Upload_obj = Upload(myfile, data)
        return Upload_obj.handle()
    return render(request, 'dataset/upload.html', {'datasetname':datasetname})

def show(request, datasetname):
    return render(request, 'dataset/show.html', {'dataset': dataset.objects.get(name=datasetname)})

def download(request, datasetname):
    return render(request, 'dataset/download.html', {'dataset': dataset.objects.get(name=datasetname)})
