"""firstProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from firstApp import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', include('firstApp.urls')),
    url(r'^player/(?P<id>\d+)/$', views.playerView.as_view()),
    url(r'^season/(?P<id>\d+)/$', views.scheduleView.as_view()),
    url(r'^runs-match/(?P<id>\d+)/$', views.runsMatchView.as_view()),
    url(r'^match/(?P<id>\d+)/$', views.matchView.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^help/', views.test.as_view()),
    url(r'^mom/', views.manOfTheMatchView.as_view()),
    url(r'^captain/', views.captainView.as_view()),
    url(r'^api/', views.playerView.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
