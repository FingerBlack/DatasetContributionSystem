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
                            deadline=deadline,
                            dataset=dataset_obj,
                            description=description,
                            pv=0,
                            amount=amount,
                            owner=request.user)
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
    try:
        task_tmp = task.objects.get(id=taskid)
    except:
        return HttpResponseRedirect('/task/')
    if task_tmp.owner == request.user:
        task_tmp.delete()
        return render(request, 'success.html', {'title': '删除任务成功'})
    return HttpResponseRedirect('/task/')


@login_required
def change(request, datasetname, taskid):
    if request.method == "POST":
        name = request.POST.get("name", '')
        deadline = request.POST.get("deadline", '')
        description = request.POST.get('description', '')
        amount = request.POST.get('amount', '')
        task_tmp = task.objects.get(id=taskid)
        task_tmp.name = name
        task_tmp.deadline = deadline
        task_tmp.description = description
        task_tmp.amount = amount
        task_tmp.save()
        return render(request, 'success.html', {'title': '修改任务成功'})
    return render(request, 'task/change.html', {'task': task.objects.get(id=taskid)})
