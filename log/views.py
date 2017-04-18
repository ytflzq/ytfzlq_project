# -*-coding=UTF-8-*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse
from util.database import Database
from util.formatDatetime import datetime_to_string
import os
import json
import datetime
def index(request):
    name = request.session.get('name',default=None)
    if not name:
        params={"mes":""}
        templateFile = "login.html"
        return render_to_response(
            templateFile,
            params,
            RequestContext(request)
        )
    user = request.GET.get("user")
    if not user:
        user=""
    limit = 10
    curpage = request.GET.get('curpage',None)
    if not curpage:
        curpage=1
    else:
        curpage =int(curpage)
    start = curpage*limit -limit
    database = Database()
    if user!="":
        row = database.select_fetchall("""SELECT user.name,log.id,log.remark,log.type,log.time 
            FROM user,log WHERE log.user_id = user.id and user.id=%s order by time desc limit %s,%s
             """, [user,start,limit])
        lenrow = database.select_fetchall("""SELECT count(log.id) len FROM log  where log.user_id = %s """, [user])
    else:
        row = database.select_fetchall("""SELECT user.name,log.id,log.remark,log.type,log.time 
            FROM user,log WHERE log.user_id =user.id order by time desc limit %s,%s
             """, [start,limit])
        lenrow = database.select_fetchall("""SELECT count(log.id) len FROM log """, [])
    for x in row:
        x['time'] = datetime_to_string(x["time"]);
    users = database.select_fetchall(""" SELECT user.name,user.id
        FROM user """,[])
    params={
        "users":users,
        "log":row,
        "count":lenrow[0]['len'],
        "curpage":curpage
    }
    templateFile = "log/index.html"
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )
def index2(request):
    name = request.session.get('name',default=None)
    if not name:
        params={"mes":""}
        templateFile = "login.html"
        return render_to_response(
            templateFile,
            params,
            RequestContext(request)
        )
    user = request.GET.get("user")
    if not user:
        user=""
    limit = 10
    curpage = request.GET.get('curpage',None)
    if not curpage:
        curpage=1
    else:
        curpage =int(curpage)
    start = curpage*limit -limit
    database = Database()
    if user!="":
        row = database.select_fetchall("""SELECT user.name,log.id,log.remark,log.type,log.time 
            FROM user,log WHERE log.user_id = user.id and user.id=%s order by time desc limit %s,%s
             """, [user,start,limit])
        lenrow = database.select_fetchall("""SELECT count(log.id) len FROM log  where log.user_id = %s """, [user])
    else:
        row = database.select_fetchall("""SELECT user.name,log.id,log.remark,log.type,log.time 
            FROM user,log WHERE log.user_id =user.id order by time desc limit %s,%s
             """, [start,limit])
        lenrow = database.select_fetchall("""SELECT count(log.id) len FROM log """, [])
    for x in row:
        x['time'] = datetime_to_string(x["time"]);
    users = database.select_fetchall(""" SELECT user.name,user.id
        FROM user """,[])
    params={
        "users":users,
        "log":row,
        "count":lenrow[0]['len'],
        "curpage":curpage
    }
    templateFile = "log/index2.html"
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )
def jsonIndex(request):
    name = request.session.get('name',default=None)
    if not name:
        params={"mes":""}
        templateFile = "login.html"
        return render_to_response(
            templateFile,
            params,
            RequestContext(request)
        )
    user = request.GET.get("user")
    if not user:
        user=""
    limit = 10
    curpage = request.GET.get('curpage',None)
    if not curpage:
        curpage=1
    else:
        curpage =int(curpage)
    start = curpage*limit -limit
    database = Database()
    if user!="":
        row = database.select_fetchall("""SELECT user.name,log.id,log.remark,log.type,log.time 
            FROM user,log WHERE log.user_id = user.id and user.id=%s order by time desc limit %s,%s
             """, [user,start,limit])
        lenrow = database.select_fetchall("""SELECT count(log.id) len FROM log  where log.user_id = %s """, [user])
    else:
        row = database.select_fetchall("""SELECT user.name,log.id,log.remark,log.type,log.time 
            FROM user,log WHERE log.user_id =user.id order by time desc limit %s,%s
             """, [start,limit])
        lenrow = database.select_fetchall("""SELECT count(log.id) len FROM log """, [])
    for x in row:
        x['time'] = datetime_to_string(x["time"]);

    data = {"row": row,"count":lenrow}
    #ensure_ascii=False用于处理中文
    return HttpResponse(json.dumps(data, ensure_ascii=False))
    pass
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