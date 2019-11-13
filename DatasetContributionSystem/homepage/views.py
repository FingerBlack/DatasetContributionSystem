from django.shortcuts import render
from .models import dataset

# Create your views here.

def index(request):
    return render(request, 'homepage/home.html', {'dataset': dataset.objects.all()})
