from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from task.models import task

# Create your views here.


def index(request):
    return render(request, 'task/task.html', {'task': task.objects.all()})

@login_required
def create(request, datasetname):
    if request.method == "POST":
        name = request.POST.get("name", '')
        deadline = request.POST.get("deadline", '')
        description = request.POST.get('description', '')
        amount = request.POST.get('amount', '')
        task.objects.create(name=name,
                            deadline=deadline[0:9],
                            related_dataset=datasetname,
                            # dataset_name=datasetname,
                            description=description,
                            pv=0,
                            amount=amount,
                            owner=request.user.username)
        return HttpResponseRedirect('/')
    return render(request, 'task/create.html')

@login_required
def show(request, datasetname, taskname):
    return render(request, 'task/show.html', {'task': task.objects.get(name=taskname)})
