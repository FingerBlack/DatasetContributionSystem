from django.shortcuts import render
def idex(request,datasetname):

    return render(request,'comment/comment.html')

def post(request,datasetname):
    return render(request,'comment/post.html')
# Create your views here.
