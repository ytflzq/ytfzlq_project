from django.conf.urls import include, url
from app import views
urlpatterns = [
    url(r'^$', views.home),
    url(r'^exit$', views.exit),
    url(r'^addComment$', views.addComment),
    url(r'^delComment/(.+)$', views.delComment),
    url(r'^statistics$', views.statistics),
    url(r'^getStatisticData$', views.getStatisticData),
    url(r'^option$', views.option),
    url(r'^jsonHome$', views.jsonHome),
    url(r'^test$', views.test),
    url(r'^index3$', views.index3),
    url(r'^jsontest$', views.jsontest),
    url(r'^new_index$', views.new_index),
]