import csv
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','firstProject.settings')

import django
django.setup()

from datetime import datetime
from firstApp.models import Season, Player, Match, Ball_by_Ball, Team, Player_Match

def date(x):
    try:
        return datetime.strptime(x, '%d-%b-%y')
    except:
        return None

def integer(x) :
    try :
        return int(x)
    except :
        return None

with open('/home/shubham/Desktop/ipl/Season.csv','r') as f:
    reader = csv.DictReader(f)  #DictWriter
    for row in reader:

        t = Season.objects.get_or_create (
        Season_Id = integer(row['Season_Id']),
        Season_Year = integer(row['Season_Year']),
        Orange_Cap_Id = integer(row['Orange_Cap_Id']),
        Purple_Cap_Id = integer(row['Purple_Cap_Id']),
        Man_of_the_Series_Id = integer(row['Man_of_the_Series_Id']))


print (1)

with open('/home/shubham/Desktop/ipl/Player.csv','r') as f:
    reader = csv.DictReader(f)  #DictWriter
    for row in reader:

        t = Player.objects.get_or_create (
        Player_Id = integer (row['Player_Id']),
        Player_Name = row['Player_Name'],
        DOB = date(row['DOB']),
        Batting_Hand = row['Batting_Hand'],
        Bowling_Skill = row['Bowling_Skill'],
        Country = row['Country'],
        Is_Umpire = integer (row['Is_Umpire']))

print (2)

with open('/home/shubham/Desktop/ipl/Match.csv','r') as f:
    reader = csv.DictReader(f)  #DictWriter
    for row in reader:

        t = Match.objects.get_or_create (
        Match_Id = integer(row['Match_Id']),
        Match_Date = date(row['Match_Date']),
        Team_Name_Id = integer(row['Team_Name_Id']),
        Opponent_Team_Id = integer(row['Opponent_Team_Id']),
        Season_Id = integer(row['Season_Id']),
        Venue_Name = row['Venue_Name'],
        Toss_Winner_Id = integer(row['Toss_Winner_Id']),
        Toss_Decision = row['Toss_Decision'],
        IS_Superover = integer(row['IS_Superover']),
        IS_Result = integer(row['IS_Result']),
        Is_DuckWorthLewis = integer(row['Is_DuckWorthLewis']),
        Win_Type = row['Win_Type'],
        Won_By = integer(row['Won_By']),
        Match_Winner_Id = integer(row['Match_Winner_Id']),
        Man_Of_The_Match_Id = integer(row['Man_Of_The_Match_Id']),
        First_Umpire_Id = integer(row['First_Umpire_Id']),
        Second_Umpire_Id = integer(row['Second_Umpire_Id']),
        City_Name = row['City_Name'],
        Host_Country = row['Host_Country'])

print (3)
#
with open('/home/shubham/Desktop/ipl/Team.csv','r') as f:
    reader = csv.DictReader(f)  #DictWriter
    for row in reader:

        t = Team.objects.get_or_create (
        Team_Id = integer (row['Team_Id']),
        Team_Name = row['Team_Name'],
        Team_Short_Code = row['Team_Short_Code'])

print (4)

with open('/home/shubham/Desktop/ipl/Player_Match.csv','r') as f:
    reader = csv.DictReader(f)  #DictWriter
    for row in reader:

        t = Player_Match.objects.get_or_create (
        Match_Id = integer(row['Match_Id']),
        Player_Id = integer(row['Player_Id']),
        Team_Id = integer(row['Team_Id']),
        Is_Keeper = integer(row['Is_Keeper']),
        Is_Captain = integer(row['Is_Captain']))


with open('/home/shubham/Documents/index.csv','r') as f:
    reader = csv.DictReader(f)  #DictWriter
    count = 0
    for row in reader:

        t = Ball_by_Ball.objects.get_or_create (
        Match_Id = integer (row['Match_Id']),
        Innings_Id = integer (row['Innings_Id']),
        Over_Id = integer (row['Over_Id']),
        Ball_Id = integer (row['Ball_Id']),
        Team_Batting_Id = integer (row['Team_Batting_Id']),
        Team_Bowling_Id = integer (row['Team_Bowling_Id']),
        Striker_Id = integer (row['Striker_Id']),
        Striker_Batting_Position = integer (row['Striker_Batting_Position']),
        Non_Striker_Id = integer (row['Non_Striker_Id']),
        Bowler_Id = integer (row['Bowler_Id']),
        Batsman_Scored = integer (row['Batsman_Scored']),

        Extra_Type = row['Extra_Type'],
        Extra_Runs = integer (row['Extra_Runs']),
        Player_dissimal_Id = integer (row['Player_dissimal_Id']),
        Dissimal_Type = row['Dissimal_Type'],
        Fielder_Id = integer (row['Fielder_Id']))
        count += 1
        if count%30 == 0 :
            print (count, end = " ")

with open('/home/shubham/Desktop/djangoProjects/testProject/playerUrl.csv','r') as f:
    reader = csv.DictReader(f)  #DictWriter
    for row in reader:

        q = Player.objects.get(Player_Id = row['Player_Id'])
        q.url = (row['url'])
        q.save()
        t = Season (
        Season_Id = integer(row['Season_Id']),
        Season_Year = integer(row['Season_Year']),
        Orange_Cap_Id = integer(row['Orange_Cap_Id']),
        Purple_Cap_Id = integer(row['Purple_Cap_Id']),
        Man_of_the_Series_Id = integer(row['Man_of_the_Series_Id']))

print ('Success!!')
