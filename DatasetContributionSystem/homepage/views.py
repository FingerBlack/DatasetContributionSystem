from django.shortcuts import render
from dataset.models import dataset
from task.models import task
from django.views.decorators.cache import cache_page

# Create your views here.

@cache_page(60 * 15)
def index(request):
    return render(request, 'homepage/home.html', {'dataset': dataset.objects.all(), 'task':task.objects.all()})
