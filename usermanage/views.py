# -*-coding=UTF-8-*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import datetime
from util.database import Database
from django.http import HttpResponse
import os
import json
# import simplejson
def index(request):
    name = request.session.get('name',default=None)
    role_id = request.session.get('role_id',default=False)
    if not name:
        params={"mes":""}
        templateFile = "login.html"
        return render_to_response(
            templateFile,
            params,
            RequestContext(request)
        )
    database = Database()
    users = database.select_fetchall(""" SELECT user.name,user.id,password,role_id,sex,age
        FROM user """,[])
    params={
    "user":users,
    "role_id":role_id
    }
    templateFile = "usermanage/index.html"
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )
@csrf_exempt
def addUser(request):
    name = request.session.get('name',default=None)
    if not name:
        params={"mes":""}
        templateFile = "login.html"
        return render_to_response(
            templateFile,
            params,
            RequestContext(request)
        )
    loginname = request.POST['loginname']
    sex = request.POST['sex']
    age = request.POST['age']
    # password = request.POST['password']
    password = "123456"
    database = Database()
    row = database.execute("""INSERT `user`(name,`password`,sex,age) VALUES(%s,%s,%s,%s)
        """, [loginname,password,sex,age])
    return HttpResponseRedirect('/usermanage/index')  #跳转到index界面 
@csrf_exempt
def updateUser(request):
    name = request.session.get('name',default=None)
    if not name:
        params={"mes":""}
        templateFile = "login.html"
        return render_to_response(
            templateFile,
            params,
            RequestContext(request)
        )
    loginname = request.POST['loginname']
    id = request.POST['id']
    sex = request.POST['sex']
    age = request.POST['age']
    password = request.POST['password']
    database = Database()
    row = database.execute("""update `user` set name=%s,password=%s,sex=%s,age=%s where id=%s
        """, [loginname,password,sex,age,id])
    return HttpResponseRedirect('/usermanage/index')  #跳转到index界面  
def delUser(request,id):
    print id
    name = request.session.get('name',default=None)
    if not name:
        params={"mes":""}
        templateFile = "login.html"
        return render_to_response(
            templateFile,
            params,
            RequestContext(request)
        )
    role_id = request.session.get('role_id',default=None)
    if role_id==0:#只有操作员有权限删除
        database = Database()
        database.delOperation("user",id)
    return HttpResponseRedirect('/usermanage/index')  #跳转到index界面 
def getUser(request,id):
    print id
    database = Database()
    data = database.select_fetchall(""" SELECT user.name,user.id,sex,age,password FROM user where id=%s """,[id])
    #ensure_ascii=False用于处理中文
    return HttpResponse(json.dumps(data[0], ensure_ascii=False))
