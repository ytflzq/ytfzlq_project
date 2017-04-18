from django.conf.urls import include, url
from login import views
urlpatterns = [
    url(r'^$', views.login),
    url(r'^login_action$', views.login_action),
]