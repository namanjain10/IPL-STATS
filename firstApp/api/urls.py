from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^all-player-api/', views.allPlayersApi.as_view()),
    url(r'^player-stats-api/', views.playerStatsApi.as_view()),
    url(r'^api/', views.playerViewApi.as_view()),
    url(r'^player-name-api/',views.PlayerSearchApi.as_view()),
]
