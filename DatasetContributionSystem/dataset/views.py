from django.shortcuts import render
from .models import dataset
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.conf import settings
import django.utils.timezone as timezone
import os, zipfile, shutil, uuid, json, datetime

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


class DatasetHandler():
    #define the relation between function and type
    def upload_image_recognition(self):
        ret = {}
        try:
            zf = zipfile.ZipFile(self.file)
            zf.testzip()
        except:
            ret['status'] = '错误'
            ret['message'] = 'zip文件损坏'
            return ret
        dir_dest = os.path.join('.' + settings.MEDIA_ROOT, 'dataset', self.dataset.name)
        #check whether the dataset is empty
        if os.path.exists(dir_dest) == False:
            os.mkdir(dir_dest)
        ret['status'] = '成功'
        ret['message'] = '上传成功'
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

    def download_image_recognition(self):
        pass
    
    upload_type_to_func = {
        2: upload_image_recognition, 1: upload_image_recognition}
    download_type_to_func = {
        2: download_image_recognition, 1: download_image_recognition}

    def __init__(self, dataset):
        self.dataset = dataset

    def upload(self, file):
        self.file = file
        return HttpResponse(json.dumps(self.upload_type_to_func[self.dataset.dataType](self)))

    def download(self):
        if (timezone.now() - self.dataset.cached_time) > datetime.timedelta(seconds = 10):
            print('exceed cached time, rebuild now...')
            self.download_type_to_func[self.dataset.dataType](self)
            self.dataset.cached_time = timezone.now()
            self.dataset.save()
        fp = os.path.join('.' + settings.MEDIA_ROOT, 'dataset', self.dataset.name + '.zip')
        file = open(fp, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="download.zip"'
        return response

@login_required
def upload_view(request, datasetname):
    try:
        data = dataset.objects.get(name = datasetname)
    except:
        return render(request, 'failure.html', {'title': '所选数据集不存在'})
    if request.method == 'POST':
        myfile = request.FILES.get('file')
        dh = DatasetHandler(data)
        return dh.upload(myfile)
    return render(request, 'dataset/upload.html', {'datasetname':datasetname})

def show(request, datasetname):
    return render(request, 'dataset/show.html', {'dataset': dataset.objects.get(name=datasetname)})

@login_required
def download(request, datasetname):
    try:
        data = dataset.objects.get(name = datasetname)
    except:
        return render(request, 'failure.html', {'title': '所选数据集不存在'})
    dh = DatasetHandler(data)
    return dh.download()
    #return render(request, 'dataset/download.html', {'dataset': dataset.objects.get(name=datasetname)})
