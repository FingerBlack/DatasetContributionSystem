from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from user.models import UserProfile
from dataset.models import dataset
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
import os, uuid
from django.conf import settings
from django.http import HttpResponse, FileResponse
from PIL import Image

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
            return HttpResponseRedirect(request.GET.get('next', '/'))
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
            return render(request, 'failure.html', {'title':'注册失败', 'content':'请检查用户名与密码可用性'})
    return render(request, 'user/signup.html')

def profile_view(request, username):
    if UserProfile.objects.filter(username = username).exists():
        user = UserProfile.objects.get(username = username)
        ret = {}
        ret['user'] = UserProfile.objects.get(username = username)
        ret['dataset'] = dataset.objects.filter(owner = user)
        return render(request, 'user/profile.html', ret)
    return render(request, 'failure.html', {'title': '无此用户！'})

@login_required
def revise_view(request, username):
    if request.method == "POST":
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        description = request.POST.get('description', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        img = request.FILES.get('img')
        if check_password(old_password, request.user.password):
            try:
                if len(new_password) > 0:
                    request.user.password = make_password(new_password)
                if len(description) > 0:    
                    request.user.description = description
                if len(first_name) > 0:    
                    request.user.first_name = first_name
                if len(last_name) > 0:    
                    request.user.last_name = last_name
                try:
                    img = Image.open(img)
                except:
                    return render(request, 'failure.html', {'title':'请检查上传图片格式'})

                img_name = str(uuid.uuid4())
                img_path = os.path.join('.' + settings.MEDIA_ROOT, 'avatar')
                if not os.path.exists(img_path):
                    os.makedirs(img_path)
                img.save(os.path.join(img_path, img_name + '.jpg'))
                request.user.avatar = os.path.join(settings.MEDIA_ROOT, 'avatar', img_name + '.jpg')
                request.user.save()
                return render(request, 'success.html', {'title':'修改成功'})
            except:
                return render(request, 'failure.html', {'title':'修改失败'})
        else:
            return render(request, 'failure.html', {'title':'修改失败', 'content':'旧密码不正确'})
    return render(request, 'user/revise.html') 


def show_avatar(request, username):
    img_path = '.' + UserProfile.objects.get(username = username).avatar
    file = open(img_path, "rb")
    response = FileResponse(file)
    return response