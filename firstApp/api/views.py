from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum, Count
from django.db import connection
from django.db.models import Q
from firstApp.models import Ball_by_Ball, Match, Player, Player_Match, Season, Team
from datetime import date
from dateutil.relativedelta import relativedelta
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

class PlayerCompareApi(APIView):

	def fours (self,id,val) :
		return Ball_by_Ball.objects.filter(Striker_Id = id, Batsman_Scored = val).count()

	def runs (self,id) :
		return Ball_by_Ball.objects.filter(Striker_Id = id).aggregate(Sum('Batsman_Scored')).get('Batsman_Scored__sum')

	def matches (self,id) :
		return Player_Match.objects.filter(Player_Id = id).count()

	def wickets (self,id) :
		return Ball_by_Ball.objects.filter(Bowler_Id = id).exclude(Dissimal_Type = 'runout').aggregate(Count('Player_dissimal_Id')).get('Player_dissimal_Id__count')

	def catches (self,id) :
		return Ball_by_Ball.objects.filter(Fielder_Id = id).exclude(Dissimal_Type = 'runout').count()

	def get (self, request):

		player_id1 = Player.objects.filter(Player_Name__iexact = request.GET['player_name_1']).values().first()
		player_id2 = Player.objects.filter(Player_Name__iexact = request.GET['player_name_2']).values().first()

		player_id1['matches'] = self.matches(player_id1['Player_Id'])
		player_id2['matches'] = self.matches(player_id2['Player_Id'])
		player_id1['runs'] = self.runs(player_id1['Player_Id'])
		player_id2['runs'] = self.runs(player_id2['Player_Id'])
		player_id1['wickets'] = self.wickets(player_id1['Player_Id'])
		player_id2['wickets'] = self.wickets(player_id2['Player_Id'])
		player_id1['catches'] = self.catches(player_id1['Player_Id'])
		player_id2['catches'] = self.catches(player_id2['Player_Id'])
		player_id1['fours'] = self.fours(player_id1['Player_Id'],4)
		player_id2['fours'] = self.fours(player_id2['Player_Id'],4)
		player_id1['sixes'] = self.fours(player_id1['Player_Id'],6)
		player_id2['sixes'] = self.fours(player_id2['Player_Id'],6)

		dic = [{'player1' : player_id1, 'player2' : player_id2}]

		res = json.dumps(dic, default=myconverter)
		return Response(res)

class PlayerPartnershipApi(APIView) :

    def get (self, request) :

        player_id1 = Player.objects.filter(Player_Name__iexact = request.GET['player_name_1']).values().first()
        player_id2 = Player.objects.filter(Player_Name__iexact = request.GET['player_name_2']).values().first()

        cursor = connection.cursor()
        cursor.execute(partnership.format(player_id1['Player_Id'],player_id2['Player_Id']))
        part = dictfetchall(cursor)

        try :
            part[0]['url1'] = player_id1['url']
            part[0]['url2'] = player_id2['url']
            part[0]['Player_Id1'] = player_id1['Player_Id']
            part[0]['Player_Id2'] = player_id2['Player_Id']
            part[0]['status'] = 0

        except :
            part.append({'url1' : player_id1['url'], 'url2' : player_id2['url'], 'Player_Id1' : player_id1['Player_Id'], 'Player_Id2' : player_id2['Player_Id'], 'status' : 1})

        res = json.dumps(part, default=myconverter)
        return Response(res)

class playerStatsApi(APIView):

    def get (self,request) :
        query = Player.objects.filter(Player_Name__iexact=request.GET['name']).values()
        dic = [i for i in query]

        res = json.dumps(dic, default=myconverter)
        return Response(res)
