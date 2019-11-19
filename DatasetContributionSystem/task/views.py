from django.shortcuts import render

# Create your views here.


def create(request, datasetname):
    return render(request, 'task/create.html')


def index(request):
    return render(request, 'task/task.html')
