"""ytfzlq_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib import admin
urlpatterns = [
    url(r'^app/', include('app.urls')),
    url(r'^game/', include('game.urls')),
    url(r'^login/', include('login.urls')),
    url(r'^usermanage/', include('usermanage.urls')),
    url(r'^log/', include('log.urls')),
    url(r'^task/', include('task.urls')),
    url(r'^snippets/', include('snippets.urls')),
]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
