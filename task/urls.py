from django.conf.urls import include, url
from task import views
urlpatterns = [
    url(r'^index$', views.index),
    url(r'^changeStatus$', views.changeStatus),
    url(r'^jsonIndex$', views.jsonIndex),
    url(r'^addTask$', views.addTask),
    # url(r'^login_action$', views.login_action),
]