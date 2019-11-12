from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from user.models import UserProfile

# Create your views here.
def login_view(request):
    if request.method == "POST":
        #用户登陆过程
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        print(username)
        print(password)
        user = authenticate(username = username, password = password)
        if user is not None:
            #返回用户页面
            login(request, user)
        else:
            #返回登陆失败页面
            pass
    return render(request, 'user/login.html')

def logout_view(request):
    logout(request)
    return render(request, 'user/logout.html')

def signup_view(request):
    if request.method == "POST":
        #用户注册过程
        username = request.POST.get('username', '')
        password = request.POST.get('password', '') 
        UserProfile.objects.create_user(username = username, password = password)
        return render(request, 'user/signup_success.html')
    return render(request, 'user/signup.html')