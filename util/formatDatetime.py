# -*-coding=UTF-8-*-
import datetime
# dir('ABC')
def datetime_to_string(value):
    if type(value)==datetime.datetime:
        return value.strftime('%y-%m-%d %H:%M:%S');
    # else:
        print "类型错误"
        return "";
    
