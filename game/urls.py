from django.conf.urls import include, url
from game import views
urlpatterns = [
    url(r'^snake$', views.snake),
    url(r'^gobang$', views.gobang),
]