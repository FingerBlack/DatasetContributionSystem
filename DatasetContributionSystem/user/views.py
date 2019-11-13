from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from user.models import UserProfile

# Create your views here.
def login_view(request):
    if request.method == "POST":
        #用户登陆过程
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(username = username, password = password)
        if user is not None:
            #返回用户页面
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            #返回登陆失败页面
            return render(request, 'failure.html', {'title':'登陆失败', 'content':'登陆失败，用户名或密码错误'})
    return render(request, 'user/login.html')

def logout_view(request):
    logout(request)
    return render(request, 'success.html', {'title':'登出成功'})

def signup_view(request):
    if request.method == "POST":
        #用户注册过程
        username = request.POST.get('username', '')
        password = request.POST.get('password', '') 
        email = request.POST.get('email', '')
        try:
            UserProfile.objects.create_user(username = username, password = password, email = email)
            return render(request, 'success.html', {'title':'注册成功', 'content':'恭喜你🎉，注册成功了，赶快试试下载数据集吧！'})
        except:
            return render(request, 'failure.html', {'title':'注册失败', 'content':'滚'})
    return render(request, 'user/signup.html')