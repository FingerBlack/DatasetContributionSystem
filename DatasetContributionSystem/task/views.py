from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from .models import task, dataset

# Create your views here.


def index(request):
    return render(request, 'task/task.html', {'task': task.objects.all()})

@login_required
def create(request, datasetname):
    if request.method == "POST":
        dataset_obj = dataset.objects.get(name=datasetname)
        name = request.POST.get("name", '')
        deadline = request.POST.get("deadline", '')
        description = request.POST.get('description', '')
        amount = request.POST.get('amount', '')
        task.objects.create(name=name,
                            deadline=deadline[0:9],
                            dataset=dataset_obj,
                            description=description,
                            pv=0,
                            amount=amount,
                            owner=request.user.username)
        return render(request, 'success.html', {'title':'创建任务成功'})
    return render(request, 'task/create.html')

@login_required
def show(request, datasetname, taskid):
    task_tmp = task.objects.get(id=taskid)
    task_tmp.pv += 1
    task_tmp.save()
    return render(request, 'task/show.html', {'task': task.objects.get(id=taskid)})

@login_required
def delete(request, datasetname, taskid):
    task_tmp = task.objects.get(id=taskid)
    if task_tmp.owner == request.user.username:
        task_tmp.delete()
    return render(request, 'task/task.html', {'task': task.objects.all()})
