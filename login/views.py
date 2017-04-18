# -*-coding=UTF-8-*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from util.database import Database
import os
import json
import datetime
def login(request):
    templateFile = "login.html"
    params={"mes":""}
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )

@csrf_exempt
def login_action(request):
    name = request.POST['name']
    password = request.POST['password']
    database = Database()
    row = database.select_fetchall("""SELECT user.name,user.id,user.role_id 
        FROM user WHERE name =%s and password = %s
         """, [name,password])
    if len(row)==0:
        params={"mes":"登录失败"}
        templateFile = "login.html"
        return render_to_response(
            templateFile,
            params,
            RequestContext(request)
        )
    else:
        # 创建或修改 session：
        request.session['name'] = name
        request.session['user_id'] = row[0]['id']
        request.session['role_id'] = row[0]['role_id']
        remark ="登录成功"
        database.execute(""" insert into log(type,user_id,remark,time)values(%s,%s,%s,%s)""",[1,row[0]['id'],remark,datetime.datetime.now()])
        params={"mes":"登录成功"}
        return HttpResponseRedirect('/app/new_index')  #跳转到index界面  
        # return HttpResponseRedirect('/app')  #跳转到index界面  