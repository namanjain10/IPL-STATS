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
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('firstApp.api.urls')),

    url(r'^maps/(?P<slug>[\w ,]+)/$',views.MapView.as_view()),
    url(r'^wickets-match/(?P<id>\d+)/$', views.wicketsMatchView.as_view()),
    url(r'^player/(?P<id>\d+)/$', views.playerView.as_view()),
    url(r'^season/(?P<id>\d+)/$', views.seasonView.as_view()),
    url(r'^runs-match/(?P<id>\d+)/$', views.runsMatchView.as_view()),
    url(r'^match/(?P<id>\d+)/$', views.matchView.as_view()),
    url(r'^superover/', views.SuperoverView.as_view()),
    url(r'^team-home/', views.TeamHomeView.as_view()),
    url(r'^team/(?P<id>\d+)/$', views.TeamView.as_view()),
    url(r'^team-season/(?P<id>\d+)/$', views.teamSeasonView.as_view()),
    url(r'^help/', views.test.as_view()),
    url(r'^player-home/', views.PlayerHome.as_view()),
    url(r'^mom/', views.manOfTheMatchView.as_view()),
    url(r'^captain/', views.captainView.as_view()),
    url(r'^all-players/', views.allPlayersView.as_view()),
    url(r'^test/', views.testApiView)
]

# urlpatterns = format_suffix_patterns(urlpatterns)
