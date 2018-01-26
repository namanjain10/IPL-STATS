from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum
from django.db import connection
from django.views import View
from django.db.models import Q
from firstApp.models import Ball_by_Ball, Match, Player, Player_Match, Season, Team
#from .serializer import PlayerSerializer
from datetime import date
from dateutil.relativedelta import relativedelta
from firstApp.google_image import get_image_link
from firstApp.sqlCommands import *

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def myconverter(o):
    if isinstance(o, date):
        return o.__str__()


class playerViewApi(APIView) :

    def get(self, request) :

        cursor = connection.cursor()
        cursor.execute('''SELECT striker_id, player_name, sum(batsman_scored) as runs, count (*) as balls ,(cast(sum(batsman_scored) as float) / count (*) * 100) as str
        from (select * from firstApp_ball_by_ball where match_id = %d and innings_id = 1
        except
        select * from firstApp_ball_by_ball
        where match_id = %d and innings_id = 1 and (extra_type = 'wides' or extra_type = 'noballs')) as d join firstApp_player on player_id = striker_id
        group by striker_id, player_name
        ''' %(int(request.GET['match_id']), int(request.GET['match_id'])))

        pl = dictfetchall(cursor)
        return HttpResponse(json.dumps(pl))
        # serializer = PlayerSerializer(pl, many = True)
        # return Response(serializer.data)

class allPlayersApi (APIView) :
    def get (self, request, *args, **kwargs) :
        query = Player.objects.all()

        if (request.GET['category'] != '0') :
            if (request.GET['category'] == '1') :
                query = query.filter(Is_Umpire = 0)

            else :
                query = query.filter(Is_Umpire = 1)

        if (request.GET['country'] != '0') :
            query = query.filter(Country__icontains= request.GET['country'])

        query = query.values()

        dic = [i for i in query]
        res = json.dumps(dic, default=myconverter)
        return Response(res)


class seasonApi (APIView) :
    def get (self, request, *args, **kwargs) :
        season_id = kwargs['id']
        request.GET['category']


class PlayerSearchApi (APIView) :
    
    def get (self,request) :
        query = Player.objects.filter(Player_Name__contains=request.GET['name']).values()
        dic = [i for i in query]

        res = json.dumps(dic, default=myconverter)
        return Response(res)

class playerStatsApi(APIView):
    
    def get (self,request) :
        query = Player.objects.filter(Player_Name__iexact=request.GET['name']).values()
        dic = [i for i in query]

        res = json.dumps(dic, default=myconverter)
        return Response(res)                        