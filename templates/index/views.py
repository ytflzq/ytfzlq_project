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
def home(request):
    name = request.session.get('name',default=None)
    role_id = request.session.get('role_id',default=False)
    isOperation = False
    if role_id==0:
        isOperation = True
        pass
    if not name:
        params={"mes":""}
        templateFile = "login.html"
        return render_to_response(
            templateFile,
            params,
            RequestContext(request)
        )
    title = request.GET.get("title")
    user = request.GET.get("user")
    if not title:
        title="%%"
    if not user:
        user=""
    database = Database()
    limit = 10
    curpage = request.GET.get('curpage',None)
    if not curpage:
        curpage=1
    else:
        curpage =int(curpage)
    start = curpage*limit -limit
    if user!="":
        row = database.select_fetchall("""SELECT comment.id,comment.title,
        comment.comment,user.name,comment.create_time
        FROM comment,user WHERE user.id = comment.user_id and comment.title like %s  and user.id = %s order by comment.create_time desc
         limit %s,%s""", [title,user,start,limit])
        lenrow = database.select_fetchall("""SELECT count(comment.id) len FROM comment  where comment.user_id = %s and comment.title like %s """, [user,title])
    else:
        row = database.select_fetchall("""SELECT comment.id,comment.title,
        comment.comment,user.name,comment.create_time
        FROM comment,user WHERE user.id = comment.user_id and comment.title like %s  order by comment.create_time desc
         limit %s,%s""", [title,start,limit])
        lenrow = database.select_fetchall("""SELECT count(comment.id) len FROM comment where comment.title like %s """, [title])
    
    for x in row:
        x['create_time'] = x['create_time'].strftime('%Y-%m-%d %H:%M:%S')
        if x['name']==name:
            x['isme']=True
        else:
            x['isme']=False
    users = database.select_fetchall(""" SELECT user.name,user.id
        FROM user """,[])

    if title=="%%":
        title=""
    params={
    "row":row,
    "count":lenrow[0]['len'],
    "curpage":curpage,
    "title":title,
    "user":user,
    "users":users,
    "name":name,
    "isOperation":isOperation,
    "openOption":True,
    "refreshTime":100
    }
    templateFile = "index/index.html"
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )
@csrf_exempt
def addComment(request):
    name = request.session.get('name',default=None)
    if not name:
        params={"mes":""}
        templateFile = "login.html"
        return render_to_response(
            templateFile,
            params,
            RequestContext(request)
        )
    title = request.POST['title']
    comment = request.POST['comment']
    name = request.session.get('name',default=None)
    dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_id =request.session['user_id']
    database = Database()
    row = database.execute("""INSERT `comment`(title,`comment`,user_id,create_time) VALUES(%s,%s,%s,%s)
        """, [title,comment,user_id,dateTime])
    return HttpResponseRedirect('/app')  #跳转到index界面  

def exit(request):
    remark = "注销"
    database = Database()
    database.execute(""" insert into log(type,user_id,remark,time)values(%s,%s,%s,%s)""",[2,request.session['user_id'],remark,datetime.datetime.now()])
    del request.session['name']
    del request.session['user_id']
    return HttpResponseRedirect('/login')  #跳转到index界面  


def statistics(request):
    name = request.session.get('name',default=None)
    if not name:
        params={"mes":""}
        templateFile = "login.html"
        return render_to_response(
            templateFile,
            params,
            RequestContext(request)
        )
    database = Database()
    row = database.select_fetchall("""SELECT COUNT(comment.id) count,user.name
    FROM user LEFT JOIN comment  on user.id = comment.user_id  GROUP BY user_id,user.name  """, [])
    count =[]
    names = [];
    for x in row:
        count.append(x['count'])
        names.append(x['name'])
    params={
    "name":name,
    "names":names,
    "count":count
    }
    templateFile = "statistics.html"
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )

def getStatisticData(request):
    name = request.session.get('name',default=None)
    if not name:
        params={"mes":""}
        templateFile = "login.html"
        return render_to_response(
            templateFile,
            params,
            RequestContext(request)
        )
    params={
    "name":name
    }
    templateFile = "statistics.html"
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )

def delComment(request,id):
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
        database.delOperation("comment",id)
    return HttpResponseRedirect('/app')  #跳转到index界面  
def option(request):
    name = request.session.get('name',default=None)
    role_id = request.session.get('role_id',default=False)
    isOperation = False
    if role_id==0:
        isOperation = True
        pass
    if not name:
        params={"mes":""}
        templateFile = "login.html"
        return render_to_response(
            templateFile,
            params,
            RequestContext(request)
        )
    title = request.GET.get("title")
    user = request.GET.get("user")
    if not title:
        title="%%"
    if not user:
        user=""
    database = Database()
    limit = 10
    curpage = request.GET.get('curpage',None)
    if not curpage:
        curpage=1
    else:
        curpage =int(curpage)
    start = curpage*limit -limit
    if user!="":
        row = database.select_fetchall("""SELECT comment.id,comment.title,
        comment.comment,user.name,comment.create_time
        FROM comment,user WHERE user.id = comment.user_id and comment.title like %s  and user.id = %s order by comment.create_time desc
         limit %s,%s""", [title,user,start,limit])
        lenrow = database.select_fetchall("""SELECT count(comment.id) len FROM comment  where comment.user_id = %s and comment.title like %s """, [user,title])
    else:
        row = database.select_fetchall("""SELECT comment.id,comment.title,
        comment.comment,user.name,comment.create_time
        FROM comment,user WHERE user.id = comment.user_id and comment.title like %s  order by comment.create_time desc
         limit %s,%s""", [title,start,limit])
        lenrow = database.select_fetchall("""SELECT count(comment.id) len FROM comment where comment.title like %s """, [title])
    
    for x in row:
        x['create_time'] = x['create_time'].strftime('%Y-%m-%d %H:%M:%S')
        if x['name']==name:
            x['isme']=True
        else:
            x['isme']=False
    users = database.select_fetchall(""" SELECT user.name,user.id
        FROM user """,[])

    if title=="%%":
        title=""
    params={
    "row":row,
    "count":lenrow[0]['len'],
    "curpage":curpage,
    "title":title,
    "user":user,
    "users":users,
    "name":name,
    "isOperation":isOperation,
    "openOption":True,
    "refreshTime":100
    }
    templateFile = "index2.html"
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )

def jsontest(request):
    data = [{"author": "Pete 33", "text": "This is one comment"},{"author": "Jordan Walke", "text": "This is *another* comment"}]
    #ensure_ascii=False用于处理中文
    return HttpResponse(json.dumps(data, ensure_ascii=False))
    pass

def jsonHome(request):
    name = request.session.get('name',default=None)
    if not name:
        params={"mes":""}
        templateFile = "login.html"
        return render_to_response(
            templateFile,
            params,
            RequestContext(request)
        )
    title = request.GET.get("title")
    user = request.GET.get("user")
    title = request.GET.get("title")
    user = request.GET.get("username")
    curpage = request.GET.get('curpage',None)
    if not title:
        title="%%"
    if not user:
        user=""
    database = Database()
    limit = 10
    if not curpage:
        curpage=1
    else:
        curpage =int(curpage)
    start = curpage*limit -limit
    if user!="":
        row = database.select_fetchall("""SELECT comment.id,comment.title,
        comment.comment,user.name,comment.create_time
        FROM comment,user WHERE user.id = comment.user_id and comment.title like %s  and user.id = %s order by comment.create_time desc
         limit %s,%s""", [title,user,start,limit])
        lenrow = database.select_fetchall("""SELECT count(comment.id) len FROM comment  where comment.user_id = %s and comment.title like %s """, [user,title])
    else:
        row = database.select_fetchall("""SELECT comment.id,comment.title,
        comment.comment,user.name,comment.create_time
        FROM comment,user WHERE user.id = comment.user_id and comment.title like %s  order by comment.create_time desc
         limit %s,%s""", [title,start,limit])
        lenrow = database.select_fetchall("""SELECT count(comment.id) len FROM comment where comment.title like %s """, [title])
    for x in row:
        x['create_time'] = x['create_time'].strftime('%Y-%m-%d %H:%M:%S')

    data = {"row": row,"count":lenrow}
    #ensure_ascii=False用于处理中文
    return HttpResponse(json.dumps(data, ensure_ascii=False))
    pass
def test(request):
    name = request.session.get('name',default=None)
    if not name:
        params={"mes":""}
        templateFile = "login.html"
        return render_to_response(
            templateFile,
            params,
            RequestContext(request)
        )
    params={
    "name":name
    }
    templateFile = "test.html"
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )
def index3(request):
    name = request.session.get('name',default=None)
    role_id = request.session.get('role_id',default=False)
    isOperation = False
    if role_id==0:
        isOperation = True
        pass
    if not name:
        params={"mes":""}
        templateFile = "login.html"
        return render_to_response(
            templateFile,
            params,
            RequestContext(request)
        )
    title = request.GET.get("title")
    user = request.GET.get("user")
    if not title:
        title="%%"
    if not user:
        user=""
    database = Database()
    limit = 10
    curpage = request.GET.get('curpage',None)
    if not curpage:
        curpage=1
    else:
        curpage =int(curpage)
    start = curpage*limit -limit
    if user!="":
        row = database.select_fetchall("""SELECT comment.id,comment.title,
        comment.comment,user.name,comment.create_time
        FROM comment,user WHERE user.id = comment.user_id and comment.title like %s  and user.id = %s order by comment.create_time desc
         limit %s,%s""", [title,user,start,limit])
        lenrow = database.select_fetchall("""SELECT count(comment.id) len FROM comment  where comment.user_id = %s and comment.title like %s """, [user,title])
    else:
        row = database.select_fetchall("""SELECT comment.id,comment.title,
        comment.comment,user.name,comment.create_time
        FROM comment,user WHERE user.id = comment.user_id and comment.title like %s  order by comment.create_time desc
         limit %s,%s""", [title,start,limit])
        lenrow = database.select_fetchall("""SELECT count(comment.id) len FROM comment where comment.title like %s """, [title])
    
    for x in row:
        x['create_time'] = x['create_time'].strftime('%Y-%m-%d %H:%M:%S')
        if x['name']==name:
            x['isme']=True
        else:
            x['isme']=False
    users = database.select_fetchall(""" SELECT user.name,user.id
        FROM user """,[])

    if title=="%%":
        title=""
    params={
    "row":row,
    "count":lenrow[0]['len'],
    "curpage":curpage,
    "title":title,
    "user":user,
    "users":users,
    "name":name,
    "isOperation":isOperation,
    "openOption":True,
    "refreshTime":100
    }
    templateFile = "index3.html"
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )
def new_index(request):
    name = request.session.get('name',default=None)
    params={
    "name":name
    }
    templateFile = "index/new_index.html"
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )