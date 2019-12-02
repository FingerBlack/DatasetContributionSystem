from django.shortcuts import render
from .models import dataset, datasetFileIndex, transaction, userBuyDataset
from user.models import UserProfile
from task.models import task
from comment.models import star
from django.db import transaction as db_transaction
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.conf import settings
import django.utils.timezone as timezone
import os, zipfile, shutil, uuid, json, datetime
from django.views.decorators.cache import cache_page

# Create your views here.
def index(request):
    data = dataset.objects.all()
    for item in data:
        if request.user.is_authenticated:
            if userBuyDataset.objects.filter(user = request.user, dataset = item).exists():
                item.bought = True
            else:
                item.bought = False
        else:
            item.bought = False
    return render(request, 'dataset/dataset.html', {'dataset': data})

@login_required
def create(request):
    if request.method == "POST":
        name = request.POST.get("name", '')
        price = float(request.POST.get("price", ''))
        datatype = request.POST.get("datatype", '')
        description = request.POST.get('description', '')
        data = dataset.objects.create(name=name, 
                               price=price, 
                               dataType=datatype, 
                               description=description,
                               owner=request.user)
        dir_dest = os.path.join('.' + settings.MEDIA_ROOT, 'dataset', str(data.id))
        if os.path.exists(dir_dest) == False:
            os.mkdir(dir_dest)
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
            with open(os.path.join(self.dir_dest, targetName + '.jpg'), 'wb') as f:
                size += f.write(zf.read('.'.join(fn_jpg)))
            with open(os.path.join(self.dir_dest, targetName + '.txt'), 'wb') as f:
                size += f.write(zf.read('.'.join(fn_txt)))
            datasetFileIndex.objects.create(name = self.dataset, filename = targetName, owner = self.user, size = size)
            self.dataset.size += size
        self.dataset.save()
        return ret
    def download_image_with_tag(self):
        fp = self.dir_dest + '.zip'
        zf = zipfile.ZipFile(fp, 'w', zipfile.zlib.DEFLATED)
        for item in datasetFileIndex.objects.filter(name = self.dataset):
            fp2 = os.path.join(self.dir_dest, item.filename + '.jpg')
            zf.write(fp2, './' + self.dataset.name + '/' + item.filename + '.jpg')
            fp2 = os.path.join(self.dir_dest, item.filename + '.txt')
            zf.write(fp2, './' + self.dataset.name + '/' + item.filename + '.txt')
        zf.close()
    def delete_image_with_tag(self):
        ret = {}
        obj = datasetFileIndex.objects.get(id = self.id)
        fn1 = os.path.join(self.dir_dest, obj.filename + '.jpg')
        fn2 = os.path.join(self.dir_dest, obj.filename + '.txt')
        os.remove(fn1)
        os.remove(fn2)
        self.dataset.size -= obj.size
        self.dataset.save()
        obj.delete()
        ret['status'] = 'ok'
        return ret

    def upload_image_without_tag(self):
        ret = {}
        try:
            zf = zipfile.ZipFile(self.file)
            zf.testzip()
        except:
            ret['status'] = '错误'
            ret['message'] = 'zip文件损坏'
            return ret
        ret['status'] = '成功'
        ret['message'] = '上传成功'
        ret['acceptFileList'] = []
        for item in zf.infolist():
            fn_jpg = item.filename.split('.')
            if fn_jpg[-1] != 'jpg':
                #ignore the file
                continue
            ret['acceptFileList'].append('.'.join(fn_jpg))
            targetName = str(uuid.uuid4())
            size = 0
            with open(os.path.join(self.dir_dest, targetName + '.jpg'), 'wb') as f:
                size += f.write(zf.read('.'.join(fn_jpg)))
            datasetFileIndex.objects.create(name = self.dataset, filename = targetName, owner = self.user, size = size)
            self.dataset.size += size
        self.dataset.save()
        return ret
    def download_image_without_tag(self):
        fp = self.dir_dest + '.zip'
        zf = zipfile.ZipFile(fp, 'w', zipfile.zlib.DEFLATED)
        for item in datasetFileIndex.objects.filter(name = self.dataset):
            fp2 = os.path.join(self.dir_dest, item.filename + '.jpg')
            zf.write(fp2, './' + self.dataset.name + '/' + item.filename + '.jpg')
        zf.close()
    def delete_image_without_tag(self):
        ret = {}
        obj = datasetFileIndex.objects.get(id = self.id)
        fn1 = os.path.join(self.dir_dest, obj.filename + '.jpg')
        os.remove(fn1)
        self.dataset.size -= obj.size
        self.dataset.save()
        obj.delete()
        ret['status'] = 'ok'
        return ret

    upload_type_to_func = {
        1: upload_image_with_tag, 2: upload_image_without_tag}
    download_type_to_func = {
        1: download_image_with_tag, 2: download_image_without_tag}
    delete_type_to_func = {
        1: delete_image_with_tag, 2: delete_image_without_tag}

    def __init__(self, user, dataset):
        self.user = user
        self.dataset = dataset
        self.dir_dest = os.path.join('.' + settings.MEDIA_ROOT, 'dataset', str(self.dataset.id))

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
        fp = self.dir_dest + '.zip'
        if os.path.exists(fp) == False:
            print('not exists, build now...')
            self.download_type_to_func[self.dataset.dataType](self)
            self.dataset.cached_time = timezone.now()
            self.dataset.save()
        file = open(fp, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="' + self.dataset.name + '.zip"'
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
        taskid = request.POST.get('taskid', '')
        if taskid != '':
            taskid = int(taskid)
            print(taskid)
            pass
        dh = DatasetHandler(request.user, data)
        return dh.upload(myfile)
    return render(request, 'dataset/upload.html', {'dataset':data, 'task':task.objects.filter(dataset = data)})

def show(request, datasetname):
    try:
        data = dataset.objects.get(name = datasetname)
    except:
        return render(request, 'failure.html', {'title': '所选数据集不存在'})
    if request.user.is_authenticated and userBuyDataset.objects.filter(dataset = data, user = request.user).exists():
        user_have_bought = True
    else:
        user_have_bought = False
    if request.user.is_authenticated and star.objects.filter(DatasetName = data, Username = request.user).exists():
        have_star = 1
    else:
        have_star = -1
    data.page_view += 1
    data.save()
    return render(request, 'dataset/show.html', {'dataset': data, 'user_have_bought': user_have_bought, 'have_star': have_star})

@login_required
def download(request, datasetname):
    try:
        data = dataset.objects.get(name = datasetname)
    except:
        return render(request, 'failure.html', {'title': '所选数据集不存在'})
    if not userBuyDataset.objects.filter(dataset = data, user = request.user).exists():
        with db_transaction.atomic():
            if request.user.balance >= data.price:
                transaction.objects.create(user1 = request.user, user2 = data.owner, detail = data.name, amount = data.price)
                userBuyDataset.objects.create(user = request.user, dataset = data)
                request.user.balance -= data.price
                request.user.save()
                data.owner.balance += data.price
                data.owner.save()
            else:
                return render(request, 'failure.html', {'title': '没钱还下载，你炸了！'})
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

@login_required
def drop(request, datasetname):
    try:
        data = dataset.objects.get(name = datasetname)
    except:
        return render(request, 'failure.html', {'title': '所选数据集不存在'})
    if request.user != data.owner:
        return render(request, 'failure.html', {'title': '只有数据集的所有者可以删除数据集'})
    #删除文件
    dh = DatasetHandler(request.user, data)
    for item in datasetFileIndex.objects.filter(name = data):
        dh.delete(item.id)
    dir_dest = os.path.join('.' + settings.MEDIA_ROOT, 'dataset', str(data.id))
    #check whether the dataset is empty
    os.rmdir(dir_dest)
    data.delete()
    return render(request, 'success.html', {'title': '删除成功'})
