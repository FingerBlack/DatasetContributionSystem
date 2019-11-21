from django.shortcuts import render
from dataset.models import dataset
from task.models import task

# Create your views here.

def index(request):
    return render(request, 'homepage/home.html', {'dataset': dataset.objects.all(), 'task':task.objects.all()})
