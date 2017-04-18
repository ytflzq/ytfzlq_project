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
    user_id = request.session.get("user_id",default=None)
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
    row = database.select_fetchall("""SELECT user.name,task.id,task.task,task.status 
        FROM user,task WHERE task.user_id = user.id and task.user_id = %s  order by task.id desc limit %s,%s
         """, [user_id,start,limit])
    lenrow = database.select_fetchall("""SELECT count(task.id) len FROM task where user_id =%s """, [user_id])
    # users = database.select_fetchall(""" SELECT user.name,user.id
    #     FROM user """,[])
    params={
        "task":row,
        "count":lenrow[0]['len'],
        "curpage":curpage
    }
    templateFile = "task/index.html"
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )
def jsonIndex(request):
    name = request.session.get('name',default=None)
    user_id = request.session.get("user_id",default=None)
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
    row = database.select_fetchall("""SELECT user.name,task.id,task.task,task.status 
        FROM user,task WHERE task.user_id = user.id and task.user_id = %s  order by task.id desc limit %s,%s
         """, [user_id,start,limit])
    lenrow = database.select_fetchall("""SELECT count(task.id) len FROM task where user_id =%s """, [user_id])
    data = {"row": row,"count":lenrow}
    #ensure_ascii=False用于处理中文
    return HttpResponse(json.dumps(data, ensure_ascii=False))
    pass
@csrf_exempt
def changeStatus(request):
    id = request.POST.get('id',None)
    type = request.POST.get('type',None)
    if id and type :
        database = Database()
        if type == "start":
            database.execute(""" update task set status = %s where id = %s """,[1,id])
        if type == "success":
            database.execute(""" update task set status = %s where id = %s """,[2,id])
        if type == "fail":
            database.execute(""" update task set status = %s where id = %s """,[3,id])
        return HttpResponse(json.dumps(["success"], ensure_ascii=False))
    else: 
        return HttpResponse(json.dumps(["failed"], ensure_ascii=False))
@csrf_exempt
def addTask(request):
    name = request.session.get('name',default=None)
    user_id = request.session.get('user_id',default=None)
    if not name:
        params={"mes":""}
        templateFile = "login.html"
        return render_to_response(
            templateFile,
            params,
            RequestContext(request)
        )
    task = request.POST['task']
    database = Database()
    row = database.execute("""INSERT `task`(task,`status`,user_id) VALUES(%s,%s,%s)
        """, [task,0,user_id])
    return HttpResponseRedirect('/task/index')  #跳转到index界面 