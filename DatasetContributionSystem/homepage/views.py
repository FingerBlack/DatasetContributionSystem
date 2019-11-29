from django.shortcuts import render
from dataset.models import dataset
from task.models import task
from django.views.decorators.cache import cache_page

# Create your views here.

def index(request):
    data = dataset.objects.all().order_by('-star')
    if data.count() > 5:
        data = data[:5]
    return render(request, 'homepage/home.html', {'dataset': data, 'task':task.objects.all()})
