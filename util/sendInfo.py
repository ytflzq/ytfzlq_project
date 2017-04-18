import urllib, urllib2, sys


host = 'http://sms.market.alicloudapi.com'
path = '/singleSendSms'
method = 'GET'
appcode = '你自己的AppCode'
querys = 'ParamString=%7B%22no%22%3A%22123456%22%7D&RecNum=RecNum&SignName=SignName&TemplateCode=TemplateCode'
bodys = {}
url = host + path + '?' + querys

request = urllib2.Request(url)
request.add_header('Authorization', 'APPCODE ' + appcode)
response = urllib2.urlopen(request)
content = response.read()
if (content):
    print(content)