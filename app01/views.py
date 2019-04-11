from django.shortcuts import render, HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
import os,json
from app01 import models
from django.views import View
from django.utils.safestring import mark_safe
# from utils import pagination
from django.utils.decorators import method_decorator

# Create your views here.

def auth(func):
    def inner(request,*args,**kwargs):
        v = request.COOKIES.get('username')
        if not v:
            return redirect('/app01/login/')
        return func(request,*args,**kwargs)
    return inner

def login(request):
    if request.method == "GET":
        return render(request,"login.html")
    elif request.method == "POST":
        error_msg = ""
        user = request.POST.get("user",None)
        pwd = request.POST.get("pwd",None)
        error_msg = ""
        obj = models.User.objects.filter(username=user, userpwd=pwd).first()
        if obj:
            res = redirect('/app01/index/')
            res.set_cookie('username', user)
            return res
        else:
            error_msg = "用户名或密码错误"
            return render(request, "login.html", {"error_msg": error_msg})



@auth
def index(request):
    v = request.COOKIES.get('username')
    return render(request,"index.html",{"current_user":v})

@auth
def introduce(request):
    v = request.COOKIES.get('username')
    return render(request, "introduce.html")

@auth
def host_list(request):
    HOST_LIST = []
    host_info = models.Host.objects.all()
    for i in host_info:
        temp = {"hostname": i.hostname, "ip": i.ip,"port":i.port,"business":Application.objects.get(id=i.b_id).name}
        HOST_LIST.append(temp)
    return render(request, "host_list.html",{"host_list":HOST_LIST})

@auth
def ajax_host_add(request):
    ret = {"status":True,'error':None,'data':None}
    try:
        mes_error = ""
        h = request.POST.get("hostname")
        ip = request.POST.get("ip")
        port = request.POST.get("port")
        b_id = request.POST.get("b_id")
        #print(h,ip,port,b_id)
        if h and len(h) > 5:
            models.Host.objects.create(hostname=h,
                                       ip=ip,
                                       port=port,
                                       b_id=b_id)
        else:
            ret["status"] = False
            ret["error"] = "太短了"
    except Exception as e :
        ret["status"] = False
        ret["error"] = "请求错误"
    return HttpResponse(json.dumps(ret))
#
# def add_win(request):
#     error_msg = ""
#     if request.method == "POST":
#         #获取用户提交的数据，POST请求
#         hostname = request.POST.get("hostname")
#         hostid = request.POST.get("hostid")
#         ip = request.POST.get("ip")
#         port = request.POST.get("port")
#         operation = request.POST.get("operation")
#         status = request.POST.get("status")
#         hostaddr = request.POST.get("hostaddr")
#         hosttype = request.POST.get("hosttype")
#         # print(hostid,hostname,ip,port,operation,status,hostaddr,hosttype)
#         if hostname and hostid and ip and port and operation and status and hostaddr and hosttype:
#             data = init_db.Host(hostname=hostname,hostid=hostid,ip=ip,port=port,operation=operation,status=status,hostaddr=hostaddr,hosttype=hosttype)
#             session.add(data)
#             session.commit()
#         else:
#             error_msg = "所有填写项目均不能为空"
#         return render(request, "add_win.html", {"error_msg": error_msg})
#     return render(request, "add_win.html")
#
#
# def del_host(request):
#     if request.method == "GET":
#         nid = request.GET.get("nid")
#         # print(nid)
#         session.query(init_db.Host).filter(init_db.Host.id == nid).delete()
#         session.commit()
#     return redirect("/host_list")

def init_db(request):
    models.User.objects.create(
        username='admin',
        userpwd='123123',
        permissions='1',
    )

    return HttpResponse("orm")