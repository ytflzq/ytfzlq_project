from django.conf.urls import include, url
from log import views
urlpatterns = [
    url(r'^index$', views.index),
    url(r'^index2$', views.index2),
    url(r'^jsonIndex$', views.jsonIndex),
    # url(r'^login_action$', views.login_action),
]