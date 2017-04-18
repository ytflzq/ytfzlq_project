from django.conf.urls import include, url
from usermanage import views
urlpatterns = [
    url(r'^index$', views.index),
    url(r'^delUser/(.+)$', views.delUser),
    url(r'^getUser/(.+)$', views.getUser),
    url(r'^updateUser$', views.updateUser),
    url(r'^addUser$', views.addUser),

]