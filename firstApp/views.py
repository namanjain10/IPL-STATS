from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum
from django.db import connection
from django.views import View
from django.db.models import Q
from .models import Ball_by_Ball, Match, Player, Player_Match, Season, Team
#from .serializer import PlayerSerializer
from datetime import date
from dateutil.relativedelta import relativedelta
from .google_image import get_image_link
from .sqlCommands import *

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def index (request):
    cursor = connection.cursor()
    cursor.execute(partnership.format(1,2))
    part = dictfetchall(cursor)
    return render(request,'firstApp/index.html',{'part':part})

def testApiView(request) :
    return render(request, 'firstApp/api.html')

class SuperoverView (View) :

    def get (self, request) :
        cursor = connection.cursor()
        cursor.execute ('''
        SELECT firstApp_match.match_id, match_date
        from firstApp_ball_by_ball join firstApp_match on firstApp_match.match_id = firstApp_ball_by_ball.match_id
        where innings_id = 3 or innings_id = 4
        group by firstApp_match.match_id, match_date
        ''')
        superover = dictfetchall(cursor)
        return render (request, 'firstApp/superover.html', {'superover':superover} )

class MapView(View):
    def get (self, request, *args, **kwargs) :
        a = request.GET['stadium']
        b = request.GET['place']

        print (a,b)
        content = {'st_name' : a, 'place' : b}
        return render (request,"firstApp/maps.html",content)

class playerView (View) :
    def get (self, request, *args, **kwargs) :
        player_id = kwargs['id']
        cursor = connection.cursor()

        query = Player.objects.filter(Player_Id = player_id).values()
        player = [i for i in query]

        player[0]['age_years'] = relativedelta(date.today(),player[0]['DOB']).years
        player[0]['age_months'] = relativedelta(date.today(),player[0]['DOB']).months
        player[0]['age_days'] = relativedelta(date.today(),player[0]['DOB']).days
        player[0]['image_link'] = player[0]['url']


        cursor.execute(player_season%(int(player_id), int(player_id), int(player_id), int(player_id), int(player_id)))

        score = dictfetchall(cursor)

        cursor.execute(fifty_season_player%(int(player_id), 50, 100))
        fifty = dictfetchall(cursor)

        cursor.execute(fifty_season_player%(int(player_id), 100, 200))
        hundred = dictfetchall(cursor)

        cursor.execute(highest_season%(int(player_id)))
        highest = dictfetchall(cursor)

        cursor.execute(season_bowling.format(int(player_id)))
        bowling = dictfetchall(cursor)

        for i in range (len(score)) :
            for j in range (len(fifty)) :
                if score[i]['season_id'] == fifty[j]['Season_Id'] :
                    score[i]['fifty'] = fifty[j]['hundreds']
                    break

            for j in range (len(hundred)) :
                if score[i]['season_id'] == hundred[j]['Season_Id'] :
                    score[i]['hundred'] = hundred[j]['hundreds']
                    break

            for j in range (len(highest)) :
                if score[i]['season_id'] == highest[j]['Season_Id'] :
                    score[i]['highest'] = highest[j]['highest']
                    break

        context = {'player' : player, 'score' : score, 'bowling':bowling}
        return render(request, "firstApp/player.html", context)

class matchView (View) :
    def get (self, request, *args, **kwargs) :

        match_id = kwargs['id']
        cursor = connection.cursor()

        query = Match.objects.filter(Match_Id = match_id).values()
        match_details = [i for i in query]

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

            query = Ball_by_Ball.objects.filter(Match_Id = match_id, Player_dissimal_Id = batting[i]['Striker_Id']).values()
            outs = [i for i in query]

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

        name = Player.objects.filter(Player_Id = int(player_id)).get()
        name = name.Player_Name
        cursor = connection.cursor()

        cursor.execute(runs_per_match_player %(int(player_id),int(player_id),int(player_id),int(player_id)))

        runs = dictfetchall(cursor)

        for j in range (len(runs)) :

            for i in ('bowler_id','fielder_id') :

                if runs[j][i] :
                    runs[j][i] = Player.objects.filter(Player_Id = runs[j][i]).values('Player_Name')[0]['Player_Name']

        context = {'name' : name, 'runs' : runs}
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

class allPlayersView (View) :
    def get (self, request, *args, **kwargs) :
        return render(request, 'firstApp/all_players.html')

class seasonView (View) :
    def get (self, request, *args, **kwargs) :

        season_id = kwargs['id']
        name = Season.objects.filter(Season_Id = int(season_id)).get()
        year = name.Season_Year

        cursor = connection.cursor()

        dic = Match.objects.filter(Season_Id = season_id).order_by('Match_Date').values()
        match_details = [i for i in dic]

        for j in range (len(match_details)) :
            for i in ('Team_Name_Id','Opponent_Team_Id') :
                match_details[j][i] = (Team.objects.filter(Team_Id = match_details[j][i]).values('Team_Name')[0]['Team_Name'])

        cursor.execute(most_runs_season%int(season_id))
        runs = dictfetchall(cursor)

        cursor.execute(most_six_season%(4, int(season_id)))
        four = dictfetchall(cursor)

        cursor.execute(most_six_season%(6, int(season_id)))
        six = dictfetchall(cursor)

        cursor.execute(higest_season%int(season_id))
        highest = dictfetchall(cursor)

        cursor.execute(strike_rate_season%(int(season_id), int(season_id)))
        strike = dictfetchall(cursor)

        cursor.execute(fifty_season%(int(season_id),50,100))
        fifty = dictfetchall(cursor)

        cursor.execute(fifty_season%(int(season_id),100,200))
        hundred = dictfetchall(cursor)

        cursor.execute(four_innings_season%(4,int(season_id)))
        four_innings = dictfetchall(cursor)

        cursor.execute(four_innings_season%(6,int(season_id)))
        six_innings = dictfetchall(cursor)

        context = {'year' : year,'match_details' : match_details, 'runs' : runs, 'four' : four, 'six' : six, 'highest' : highest, 'strike' : strike, 'fifty' : fifty, 'hundred' : hundred, 'four_innings' : four_innings, 'six_innings' : six_innings}

        return render(request, "firstApp/season.html", context)

class PlayerHome (View) :
    def get (self, request, *args, **kwargs) :
        return render(request, "firstApp/player_home.html")

class TeamHomeView (View) :
    def get (self, request, *args, **kwargs) :
        query = Team.objects.all().values()
        dic = [i for i in query]

        return render(request, "firstApp/team_home.html", {'team' : dic})

class TeamView (View) :
    def get (self, request, *args, **kwargs) :
        team_id = kwargs['id']
        name = Team.objects.filter(Team_Id = int(team_id)).get()
        name = name.Team_Name

        cursor = connection.cursor()

        cursor.execute(wins.format(int(team_id)))

        # query = Match.objects.filter(Q(Team_Id = team_id) | Q(Opponent_Team_Id = team_id), Match_Winner_Id = team_id).values()

        # win = [i for i in query]
        win = dictfetchall(cursor)

        cursor.execute(losses.format(int(team_id)))
        loss = dictfetchall(cursor)

        cursor.execute(nr.format(int(team_id)))
        Nr = dictfetchall(cursor)

        for i in range (len(loss)) :
            for j in range (len(win)) :
                if loss[i]['Season_Id'] == win[j]['Season_Id'] :
                    if win[j]['wins'] == None :
                        win[j]['wins'] = 0

                    loss[i]['wins'] = win[j]['wins']
                    break
            if loss[i]['losses'] == None :
                loss[i]['losses'] = 0

            for j in range (len(Nr)) :
                if loss[i]['Season_Id'] == Nr[j]['Season_Id'] :
                    if Nr[j]['nr'] == None :
                        Nr[j]['nr'] = 0

                    loss[i]['nr'] = Nr[j]['nr']
                    break
        # wins = Match.objects.filter(Match_Winner_Id = team_id).aggregate('Season_Id').count()
        #
        # loss = (Match.objects.filter(Team_Name_Id = team_id) | Match.objects.filter(Opponent_Team_Id = team_id)).filter(IS_Result = 1).exclude(Match_Winner_Id = team_id).count()
        #
        # NR = (Match.objects.filter(Team_Name_Id = team_id) | Match.objects.filter(Opponent_Team_Id = team_id)).exclude(IS_Result = 1).count()
        #
        # dic = {'win' : wins, 'loss' : loss, 'NR' : NR}
        i = 0
        while i != len(loss) :
            loss[i]['total'] = loss[i]['wins'] + loss[i]['losses'] + loss[i]['nr']

            if loss[i]['total'] == 13 :
                loss[i]['nr'] += 1
                loss[i]['total'] = 14

            if loss[i]['total'] == 0 :
                del loss[i]
                i = i-1
            i += 1
        dic = loss
        return render (request, 'firstApp/team.html', {'name': name,'team' : dic})

class wicketsMatchView (View) :
    def get (self, request, *args, **kwargs) :
        player_id = kwargs['id']

        name = Player.objects.filter(Player_Id = int(player_id)).get()
        name = name.Player_Name

        cursor = connection.cursor()
        cursor.execute(per_match_bowling.format(int(player_id)))
        bowl = dictfetchall(cursor)
        return render (request, 'firstApp/wickets_per_match.html', {'bowl': bowl, 'name':name})

class Compare (View) :
    def get (self, request, *args, **kwargs) :
        return render(request, "firstApp/compare_players.html")

class Partnership (View) :
    def get (self, request, *args, **kwargs) :
        return render(request, "firstApp/partnerships.html")

class teamSeasonView (View) :
    def get (self, request, *args, **kwargs) :
        player_id = kwargs['id']
        name = Player.objects.filter(Player_Id = int(player_id)).get()
        name = name.Player_Name
        cursor = connection.cursor()
        cursor.execute(team_season.format(int(player_id)))
        team = dictfetchall(cursor)
        return render (request, 'firstApp/team_season.html', {'team': team, 'name':name})
