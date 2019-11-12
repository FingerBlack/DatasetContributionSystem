from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'dataset/dataset.html')

def create(request):
    return render(request, 'dataset/create/create.html')