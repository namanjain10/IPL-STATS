from rest_framework import serializers
from .models import Player, Ball_by_Ball

# class PlayerSerializer (serializers.ModelSerializer) :
#     class Meta :
#         model = Ball_by_Ball
#         fields = ['Striker_Id', 'Player_Name', 'runs', 'balls' ,'str']

# arr = Season.objects.all()
# teams = Team.objects.all()
# runs = Ball_by_Ball.objects.filter(Striker_Id = 1).aggregate(Sum('Batsman_Scored'))
# pi = Player.objects.raw('SELECT player_id, player_name from firstApp_player WHERE lower (player_name) like "%har%" ')
#
# cursor = connection.cursor()
# pi = (cursor.execute('''SELECT striker_id, player_name, sum(batsman_scored) as runs, count (*) as balls ,(cast(sum(batsman_scored) as float) / count (*) * 100) as str
# from (select * from firstApp_ball_by_ball where match_id = 335988 and innings_id = 1
#   except
#   select * from firstApp_ball_by_ball
#   where match_id = 335988 and innings_id = 1 and (extra_type = 'wides' or extra_type = 'noballs')) as d join firstApp_player on player_id = striker_id
# group by striker_id, player_name '''))
#
# print (pi.dictfetchall())
