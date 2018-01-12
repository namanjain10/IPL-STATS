from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum
from django.db import connection
from django.views import View
from .models import Ball_by_Ball, Match, Player, Player_Match, Season, Team
#from .serializer import PlayerSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import date
from dateutil.relativedelta import relativedelta
from .google_image import get_image_link
from .sqlCommands import *
import json

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class playerViewApi(APIView) :

    def get(self, request) :
        print(request.data)
        cursor = connection.cursor()
        cursor.execute('''
        SELECT striker_id, player_name, sum(batsman_scored) as runs, count (*) as balls ,(cast(sum(batsman_scored) as float) / count (*) * 100) as str
        from (select * from firstApp_ball_by_ball where match_id = %d and innings_id = 1
        except
        select * from firstApp_ball_by_ball
        where match_id = %d and innings_id = 1 and (extra_type = 'wides' or extra_type = 'noballs')) as d join firstApp_player on player_id = striker_id
        group by striker_id, player_name
        ''' %(int(match), int(match)))

        # cursor.execute(''' SELECT player_in, player_name, batting_hand
        # from firstApp_player
        # ''')

        pl = dictfetchall(cursor)
        return HttpResponse(json.dumps(pl))
        # serializer = PlayerSerializer(pl, many = True)
        # return Response(serializer.data)

    def post(self, request) :
        pass

def index (request):
    team = Player.objects.all()
    cursor = connection.cursor()

    cursor.execute('''
    SELECT striker_id, player_name, sum(batsman_scored) as runs, count (*) as balls ,(cast(sum(batsman_scored) as float) / count (*) * 100) as str
    from (select * from firstApp_ball_by_ball where match_id = 335988 and innings_id = 1
    except
    select * from firstApp_ball_by_ball
    where match_id = 335988 and innings_id = 1 and (extra_type = 'wides' or extra_type = 'noballs')) as d join firstApp_player on player_id = striker_id
    group by striker_id, player_name
    ''')

    pl = dictfetchall(cursor)

    cursor.execute ('''
    SELECT firstApp_match.match_id, match_date
    from firstApp_ball_by_ball join firstApp_match on firstApp_match.match_id = firstApp_ball_by_ball.match_id
    where innings_id = 3 or innings_id = 4
    group by firstApp_match.match_id, match_date
    ''')

    superover = dictfetchall(cursor)

    cursor.execute ('''SELECT player_dissimal_id, player_name, count(*) as count
    from firstApp_ball_by_ball join firstApp_player on player_id = player_dissimal_id

    group by player_dissimal_id, player_name
    order by player_dissimal_id''')

    outs = dictfetchall (cursor)

    cursor.execute('''SELECT * from firstApp_player where Player_Id = 57''')

    k = dictfetchall(cursor)

    my_dict = {'pi' : pl,'SuperOver' : superover,'outs' : outs , 'k' : k}
    return render(request,'firstApp/index.html',context = my_dict)

def help (request) :
    #my_dict = {'index':'OK lets do this!!'}
    return HttpResponse("Help")

class playerView (View) :
    def get (self, request, *args, **kwargs) :
        player_id = kwargs['id']
        cursor = connection.cursor()
        cursor.execute('''SELECT * from firstApp_player where player_id = %d''' % int(player_id))
        player = dictfetchall(cursor)

        player[0]['age_years'] = relativedelta(date.today(),player[0]['DOB']).years
        player[0]['age_months'] = relativedelta(date.today(),player[0]['DOB']).months
        player[0]['age_days'] = relativedelta(date.today(),player[0]['DOB']).days
        player[0]['image_link'] = player[0]['url']

        context = {'player' : player}
        return render(request, "firstApp/player.html", context)

class matchView (View) :
    def get (self, request, *args, **kwargs) :

        match_id = kwargs['id']
        cursor = connection.cursor()

        cursor.execute(''' SELECT * from firstApp_match where match_id = %d''' %int(match_id))

        match_details = dictfetchall(cursor)

        for i in ('Match_Winner_Id','Team_Name_Id','Opponent_Team_Id','Toss_Winner_Id') :
            match_details[0][i] = (Team.objects.filter(Team_Id = match_details[0][i]).values('Team_Name')[0]['Team_Name'])

        cursor.execute('''
        SELECT innings_id, striker_id, player_name, sum(batsman_scored) as runs, count (*) as balls ,round((cast(sum(batsman_scored) as float) / count (*) * 100),2) as str
        from (select * from firstApp_ball_by_ball where match_id = %d
        except
        select * from firstApp_ball_by_ball
        where match_id = %d and (extra_type = 'wides' or extra_type = 'noballs')) as d join firstApp_player on player_id = striker_id
        group by striker_id, player_name, innings_id
        order by innings_id
        ''' %(int(match_id),int(match_id)))

        batting = dictfetchall(cursor)

        for i in range(len(batting)) :
            cursor.execute('''SELECT count(*) as four
            from firstApp_ball_by_ball
            where striker_id = %d and batsman_scored = 4 and match_id = %d''' %(int(batting[i]['Striker_Id']), int(match_id)))

            four = dictfetchall(cursor)

            cursor.execute('''SELECT count(*) as six
            from firstApp_ball_by_ball
            where striker_id = %d and batsman_scored = 6 and match_id = %d''' %(int(batting[i]['Striker_Id']),int(match_id)))

            six = dictfetchall(cursor)

            batting[i]['four'] = four[0]['four']
            batting[i]['six'] = six[0]['six']

            cursor.execute('''SELECT *
            from firstApp_ball_by_ball
            where match_id = %d and player_dissimal_id = %d''' % (int(match_id), int(batting[i]['Striker_Id'])))

            outs = dictfetchall(cursor)

            if len(outs) == 0 :
                batting[i]['dissimal_type'] = None

            else :
                batting[i]['dissimal_type'] = outs[0]['Dissimal_Type']
                batting[i]['fielder_id'] = outs[0]['Fielder_Id']
                batting[i]['bowler_id'] = outs[0]['Bowler_Id']


                for j in ('bowler_id','fielder_id') :
                    if batting[i][j] :
                        batting[i][j] = Player.objects.filter(Player_Id = batting[i][j]).values('Player_Name')[0]['Player_Name']


        cursor.execute(match_bowl_str %(int(match_id), int(match_id), int(match_id), int(match_id), int(match_id), int(match_id)))

        bowling = dictfetchall(cursor)

        context = {'match_details' : match_details,'batting' : batting , 'bowling' : bowling}
        return render(request, "firstApp/match.html", context)

class runsMatchView (View) :
    def get (self, request, *args, **kwargs) :
        player_id = kwargs['id']
        cursor = connection.cursor()

        cursor.execute('''SELECT  w.match_id as match_id, match_date, venue_name, city_name, bowler_id, dissimal_type, fielder_id, sum1, balls, round((cast(sum1 as float) / balls * 100),2) as str

        from (select u.match_id, match_date, venue_name, city_name, dissimal_type, bowler_id, fielder_id, sum1
        from
      (select firstApp_match.match_id, sum(batsman_scored) as sum1, match_date, city_name, venue_name
							from firstApp_ball_by_ball join firstApp_match on firstApp_match.match_id = firstApp_ball_by_ball.match_id
							where striker_id = %d and (innings_id = 1 or innings_id = 2)
							group by firstApp_match.match_id, match_date, venue_name, city_name) as u left join

      (select d.match_id, dissimal_type, bowler_id, fielder_id
	from firstApp_ball_by_ball
    	join (
            select firstApp_match.match_id, sum(batsman_scored) as sum1
			from firstApp_ball_by_ball join firstApp_match on firstApp_match.match_id = firstApp_ball_by_ball.match_id
			where striker_id = %d and (innings_id = 1 or innings_id = 2)
            group by firstApp_match.match_id) as d on (firstApp_ball_by_ball.match_id = d.match_id and player_dissimal_id = %d)
		group by d.match_id, dissimal_type, fielder_id, bowler_id
		order by d.match_id) as f
               	 on u.match_id = f.match_id
							order by u.match_id) as w
                            	join (select match_id , count(*) as balls
										from (select *
                                            from firstApp_ball_by_ball
                                            where striker_id = %d
                                            except
                                            select *
                                            from firstApp_ball_by_ball
                                            where extra_type = 'wides' or extra_type = 'noballs') as foo
                                            group by match_id) as h on w.match_id = h.match_id
                                            order by w.match_id; ''' %(int(player_id),int(player_id),int(player_id),int(player_id)))

        runs = dictfetchall(cursor)
        print (runs[2]['fielder_id'])
        print (len(runs))

        for j in range (len(runs)) :

            for i in ('bowler_id','fielder_id') :

                if runs[j][i] :
                    runs[j][i] = Player.objects.filter(Player_Id = runs[j][i]).values('Player_Name')[0]['Player_Name']

        context = {'runs' : runs}
        return render(request, "firstApp/runs_per_match.html", context)

class manOfTheMatchView (View) :
    def get (self, request, *args, **kwargs) :

        cursor = connection.cursor()
        cursor.execute ('''SELECT man_of_the_match_id, player_name, count(*) as count
        from firstApp_match join firstApp_player on player_id = man_of_the_match_id
        group by man_of_the_match_id, player_name
        order by count(*) desc''')

        man_of_the_matches = dictfetchall (cursor)

        context = {'man' : man_of_the_matches}

        return render(request,'firstApp/most_man_of_the_matches.html',context)

class captainView (View) :

    def get (self, request, *args, **kwargs) :

        cursor = connection.cursor()
        cursor.execute ('''SELECT firstApp_player_match.player_id, player_name, count(*) as total
        from firstApp_player_match join firstApp_player on firstApp_player.player_id = firstApp_player_match.player_id
        where is_captain = 1
        group by firstApp_player_match.player_id, player_name
        order by count(*) desc''')

        captain = dictfetchall (cursor)

        for i in range (len(captain)) :

            cursor.execute ('''SELECT count(*) as win
            from firstApp_match join (select match_id , team_id
            from firstApp_player_match
            where player_id = %d and is_captain = 1) as d on firstApp_match.match_id = d.match_id
            where team_id = match_winner_id''' %int(captain[i]['Player_Id']))

            win = dictfetchall (cursor)
            captain[i]['wins'] = win[0]['win']

            cursor.execute ('''SELECT count(*) as loss
            from firstApp_match join (select match_id , team_id
            from firstApp_player_match
            where player_id = %d and is_captain = 1) as d on firstApp_match.match_id = d.match_id
            where team_id != match_winner_id and is_result = 1''' %int(captain[i]['Player_Id']))

            loss = dictfetchall (cursor)
            captain[i]['loss'] = loss[0]['loss']

            cursor.execute ('''SELECT count(*) as nr
            from firstApp_match join (select match_id , team_id
            from firstApp_player_match
            where player_id = %d and is_captain = 1) as d on firstApp_match.match_id = d.match_id
            where is_result = 0''' %int(captain[i]['Player_Id']))

            nr = dictfetchall (cursor)
            captain[i]['nr'] = nr[0]['nr']

            cursor.execute ('''SELECT count(*) as toss
            from firstApp_match join (select match_id , team_id
            from firstApp_player_match
            where player_id = %d and is_captain = 1) as d on firstApp_match.match_id = d.match_id
            where toss_winner_id = team_id''' %int(captain[i]['Player_Id']))

            toss = dictfetchall (cursor)
            captain[i]['toss'] = toss[0]['toss']

            captain[i]['win_percent'] = round(captain[i]['wins']/captain[i]['total'] * 100, 2)
            captain[i]['loss_percent'] = round(captain[i]['loss']/captain[i]['total'] * 100, 2)
            captain[i]['toss_percent'] = round(captain[i]['toss']/captain[i]['total'] * 100, 2)

        context = {'captain' : captain}

        return render(request,'firstApp/captain.html',context)

class scheduleView (View) :
    def get (self, request, *args, **kwargs) :

        season_id = kwargs['id']
        cursor = connection.cursor()

        cursor.execute(''' SELECT match_id, match_date, team_name_id, opponent_team_id, venue_name, city_name, host_country from firstApp_match where season_id = %d order by match_date''' %int(season_id))

        match_details = dictfetchall(cursor)

        for j in range (len(match_details)) :
            for i in ('Team_Name_Id','Opponent_Team_Id') :
                match_details[j][i] = (Team.objects.filter(Team_Id = match_details[j][i]).values('Team_Name')[0]['Team_Name'])

        context = {'match_details' : match_details}
        return render(request, "firstApp/schedule.html", context)

def apiView(request) :
    return render(request, 'firstApp/api.html')

class test (View) :

    def get (self, request, *args, **kwargs) :

        cursor = connection.cursor()
        # cursor.execute(test_str %2)
        q = Match.objects.raw('''SELECT * from firstApp_match''')
        pl = q
        #pl = dictfetchall(cursor)
        #print (len(pl[0]['Dissimal_Type']), 'namaan')
        context = {'batting' : pl}#, 'bowling' : bowling}
        return render(request, "firstApp/help.html", context)
