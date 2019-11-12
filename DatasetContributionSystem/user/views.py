from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

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
            login(request, user)
            print("ok")
        else:
            print("invalid")
    return render(request, 'user/login.html')