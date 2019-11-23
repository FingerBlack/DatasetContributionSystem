from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
import os
from .models import List
from dataset.models import dataset
from django.core.paginator import Paginator
from task.models import task
# Create your views here.
def index(request):
    return render(request, 'querypage/query.html', {'dataset': dataset.objects.all()})

def search(request):
    if  request.method == "GET":
        x = request.GET.get("Datasetname") 
        y =request.GET.get("Taskname")
        x_list=[]
        y_list=[]
        for i in x.split(' '):
            x_list.append(i)
        for i in y.split(' '):
            y_list.append(i)
        if x !=  None:
            List.name_list = dataset.objects.all().filter(name__in = x_list)  #导入的Article模型
        elif y!= None:
            List.name_list = task.objects.all().filter(name__in = y_list)  #导入的Article模型
        return paginator(request)
        #return render(request,'querypage/result.html',context={
def paginator(request):
    #paginator = Paginator(dataset, settings.EACH_OF_NUMBER)#每10篇文章分一页
    #page_of_blogs = paginator.get_page(page_num)#get_page方法处理用户输入的错误值
    #name_list = dataset.objects.all().filter(name__contains = x)  #导入的Article模型
    p = Paginator(List.name_list,6)   #分页，6篇文章一页
    result_list = List.name_list  
    if p.num_pages <= 1:  #如果文章不足一页
        data = ''  #不需要分页按钮
    else:
        page = int(request.GET.get('page',1))  #获取请求的文章页码，默认为第一页
        add =int(request.GET.get('item',-2))
       	if add == 1:
       		page=page+1
       	elif add ==-1:
       		page=page-1
        if page <= 0 :
            page= 1
        elif page > p.num_pages:
            page= p.num_pages    
        result_list = p.page(page) #返回指定页码的页面
        left = []  # 当前页左边连续的页码号，初始值为空
        right = []  # 当前页右边连续的页码号，初始值为空
        left_has_more = False  # 标示第 1 页页码后是否需要显示省略号
        right_has_more = False  # 标示最后一页页码前是否需要显示省略号
        first = False   # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        last = False  # 标示是否需要显示最后一页的页码号。
        total_pages = p.num_pages  
        page_range = p.page_range

        if page == 1:  #如果请求第1页
            right = page_range[page:page+2]  #获取右边连续号码页
            if right[-1] < total_pages - 1:    # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
                right_has_more = True
            if right[-1] < total_pages:   # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
                last = True
        elif page == total_pages:  #如果请求最后一页
            left = page_range[(page-3) if (page-3) > 0 else 0:page-1]  #获取左边连续号码页
            if left[0] > 2:
                left_has_more = True  #如果最左边的号码比2还要大，说明其与第一页之间还有其他页码，因此需要显示省略号，通过 left_has_more 来指示
            if left[0] > 1: #如果最左边的页码比1要大，则要显示第一页，否则第一页已经被包含在其中
                first = True
        else:  #如果请求的页码既不是第一页也不是最后一页
            left = page_range[(page-3) if (page-3) > 0 else 0:page-1]   #获取左边连续号码页
            right = page_range[page:page+2] #获取右边连续号码页
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

        data = {    #将数据包含在data字典中
            'left':left,
            'right':right,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,
            'first':first,
            'last':last,
            'total_pages':total_pages,
            'page':page
        }
    return render(request,'querypage/result.html',context={
        'dataset':result_list,'data':data
    })