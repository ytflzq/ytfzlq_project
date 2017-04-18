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
def snake(request):
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
    params={
    "name":name,
    }
    templateFile = "game/snake.html"
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )


def gobang(request):
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
    params={
    "name":name,
    }
    templateFile = "game/gobang.html"
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )
