from django.shortcuts import render
from .models import dataset, datasetFileIndex
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.conf import settings
import django.utils.timezone as timezone
import os, zipfile, shutil, uuid, json, datetime
from django.views.decorators.cache import cache_page

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
                               description=description,
                               owner=request.user)
        return HttpResponseRedirect('/dataset/' + name + '/')
    return render(request, 'dataset/create.html')


class DatasetHandler():
    #define the relation between function and type
    def upload_image_with_tag(self):
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
            size = 0
            with open(os.path.join(dir_dest, targetName + '.jpg'), 'wb') as f:
                size += f.write(zf.read('.'.join(fn_jpg)))
            with open(os.path.join(dir_dest, targetName + '.txt'), 'wb') as f:
                size += f.write(zf.read('.'.join(fn_txt)))
            datasetFileIndex.objects.create(name = self.dataset, filename = targetName, owner = self.user, size = size)
            self.dataset.size += size
        self.dataset.save()
        return ret

    def download_image_with_tag(self):
        dir_dest = os.path.join('.' + settings.MEDIA_ROOT, 'dataset', self.dataset.name)
        fp = dir_dest + '.zip'
        zf = zipfile.ZipFile(fp, 'w', zipfile.zlib.DEFLATED)
        for item in datasetFileIndex.objects.filter(name = self.dataset):
            fp2 = os.path.join(dir_dest, item.filename + '.jpg')
            zf.write(fp2, './' + self.dataset.name + '/' + item.filename + '.jpg')
            fp2 = os.path.join(dir_dest, item.filename + '.txt')
            zf.write(fp2, './' + self.dataset.name + '/' + item.filename + '.txt')
        zf.close()
    
    def delete_image_with_tag(self):
        ret = {}
        dir_dest = os.path.join('.' + settings.MEDIA_ROOT, 'dataset', self.dataset.name)
        obj = datasetFileIndex.objects.get(id = self.id)
        fn1 = os.path.join(dir_dest, obj.filename + '.jpg')
        fn2 = os.path.join(dir_dest, obj.filename + '.txt')
        os.remove(fn1)
        os.remove(fn2)
        self.dataset.size -= obj.size
        self.dataset.save()
        obj.delete()
        ret['status'] = 'ok'
        return ret
    def upload_image_without_tag(self):
        pass
    def download_image_without_tag(self):
        pass
    def delete_image_without_tag(self):
        pass

    upload_type_to_func = {
        1: upload_image_with_tag, 2: upload_image_without_tag}
    download_type_to_func = {
        1: download_image_with_tag, 2: download_image_without_tag}
    delete_type_to_func = {
        1: delete_image_with_tag, 2: delete_image_without_tag}

    def __init__(self, user, dataset):
        self.user = user
        self.dataset = dataset

    def upload(self, file):
        self.file = file
        self.dataset.last_revise_time = timezone.now()
        return HttpResponse(json.dumps(self.upload_type_to_func[self.dataset.dataType](self)))

    def download(self):
        if (self.dataset.last_revise_time - self.dataset.cached_time) > datetime.timedelta(seconds = 1):
            #set eps = 1 sec to avoid mistake
            print('revise detected, rebuild now...')
            self.download_type_to_func[self.dataset.dataType](self)
            self.dataset.cached_time = timezone.now()
            self.dataset.save()
        fp = os.path.join('.' + settings.MEDIA_ROOT, 'dataset', self.dataset.name + '.zip')
        if os.path.exists(fp) == False:
            print('not exists, build now...')
            self.download_type_to_func[self.dataset.dataType](self)
            self.dataset.cached_time = timezone.now()
            self.dataset.save()
        file = open(fp, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="download.zip"'
        return response

    def delete(self, id):
        self.id = id
        return json.dumps(self.delete_type_to_func[self.dataset.dataType](self))
        

@login_required
def upload_view(request, datasetname):
    try:
        data = dataset.objects.get(name = datasetname)
    except:
        return render(request, 'failure.html', {'title': '所选数据集不存在'})
    if request.method == 'POST':
        myfile = request.FILES.get('file')
        dh = DatasetHandler(request.user, data)
        return dh.upload(myfile)
    return render(request, 'dataset/upload.html', {'datasetname':datasetname})

def show(request, datasetname):
    try:
        data = dataset.objects.get(name = datasetname)
    except:
        return render(request, 'failure.html', {'title': '所选数据集不存在'})
    data.page_view += 1
    data.save()
    return render(request, 'dataset/show.html', {'dataset': data})

@login_required
def download(request, datasetname):
    try:
        data = dataset.objects.get(name = datasetname)
    except:
        return render(request, 'failure.html', {'title': '所选数据集不存在'})
    dh = DatasetHandler(request.user, data)
    data.page_download += 1
    data.save()
    return dh.download()
    #return render(request, 'dataset/download.html', {'dataset': dataset.objects.get(name=datasetname)})

@login_required
def manage(request, datasetname):
    try:
        data = dataset.objects.get(name = datasetname)
    except:
        return render(request, 'failure.html', {'title': '所选数据集不存在'})
    return render(request, 'dataset/manage.html', {'dataset': data, 'fileIndex': datasetFileIndex.objects.filter(name = data)})

@login_required
def delete(request, datasetname):
    ret = {}
    try:
        data = dataset.objects.get(name = datasetname)
    except:
        ret['status'] = 'no such dataset'
        return HttpResponse(json.dumps(ret))
    if request.method == "POST":
        try:
            obj = datasetFileIndex.objects.get(name = data, id = request.POST.get("id", ""))
        except:
            ret['status'] = 'no such record'
            return HttpResponse(json.dumps(ret))
        if not (data.owner == request.user or obj.owner == request.user):
           ret['status'] = 'no authority'
           return HttpResponse(json.dumps(ret))
        dh = DatasetHandler(request.user, data)
        return HttpResponse(dh.delete(request.POST.get('id', '')))
    ret['status'] = 'ok'
    return HttpResponse(json.dumps(ret))