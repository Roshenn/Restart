from django.shortcuts import render
from django.conf import settings
from booktest.models import PicTest,BookInfo,Area
from django.http import HttpResponse,JsonResponse
from django.core.paginator import Paginator




def index(request):
    return render(request, 'booktest/index.html')


def static_test(request):
    return render(request, 'booktest/static.html')


def pic_upload(request):

    pic = request.FILES['pic']
    save_path = '%s/booktest/%s'%(settings.MEDIA_ROOT,pic.name)
    with open(save_path,'wb') as f:  

        
        for content in pic.chunks():
            f.write(content)
    PicTest.objects.create(pic = 'booktest/%s'%pic.name)  
    return HttpResponse("上传成功~")



def show_bookinfo(request,pindex):
    books = BookInfo.objects.all()
    Paginator_all = Paginator(books,10)  
    if pindex == '':
        pindex = 1
    else:
        pindex = int(pindex)
    book = Paginator_all.page(pindex)    page_list = Paginator_all.page_range

    return render(request,'booktest/show_bookinfo.html',{'books':book,
                                                         })

def areas(request):
    return render(request,'booktest/areas.html')


def province(request):    list = Area.objects.filter(aParent__isnull=True)
    items = []

    for item in list:
        items.append([item.id,item.areaName, item.aParent_id])
    return JsonResponse({'prov_all': items})

def city(request,provinceid):

    list = Area.objects.filter(aParent_id=provinceid)
    items = []
    for item in list:
        items.append([item.id, item.areaName, item.aParent_id])
    print(items[0])    return JsonResponse({'city_all': items})
