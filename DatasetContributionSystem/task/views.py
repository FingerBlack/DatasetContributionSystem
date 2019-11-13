from django.shortcuts import render

# Create your views here.


def index(request, datasetname):
    return render(request, 'task/create.html')
