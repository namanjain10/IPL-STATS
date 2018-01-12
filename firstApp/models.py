from django.db import models
#from django.utils import timezone
from datetime import datetime

class Season(models.Model):
    Season_Id           = models.IntegerField(primary_key=True, default = 0)
    Season_Year         = models.IntegerField()
    Orange_Cap_Id       = models.IntegerField()
    Purple_Cap_Id       = models.IntegerField()
    Man_of_the_Series_Id = models.IntegerField()

    def __str__(self) :
        return str(self.Season_Id) + ' - ' + str(self.Season_Year)

class Player(models.Model):
    Player_Id       = models.IntegerField(primary_key=True, default = 0)
    Player_Name     = models.CharField(max_length = 100)
    DOB             = models.DateField(null = True, default = datetime.now)
    Batting_Hand    = models.CharField(max_length = 100)
    Bowling_Skill   = models.CharField(max_length = 100)
    Country         = models.CharField(max_length = 100)
    Is_Umpire       = models.IntegerField()
    url             = models.URLField(blank=True)

    def __str__(self) :
        return str(self.Player_Id) +' - '+self.Player_Name

class Match(models.Model):
    Match_Id         = models.IntegerField(primary_key=True, default = 0)
    Match_Date       = models.DateField(null = True , default = datetime.now)
    Team_Name_Id     = models.IntegerField()
    Opponent_Team_Id = models.IntegerField()
    Season_Id        = models.IntegerField()
    Venue_Name       = models.CharField(max_length = 300)
    Toss_Winner_Id   = models.IntegerField()
    Toss_Decision    = models.CharField(max_length = 100)
    IS_Superover     = models.IntegerField()
    IS_Result        = models.IntegerField()
    Is_DuckWorthLewis = models.IntegerField()
    Win_Type          = models.CharField(max_length = 100)
    Won_By            = models.IntegerField(null = True)
    Match_Winner_Id   = models.IntegerField(null = True)
    Man_Of_The_Match_Id = models.IntegerField(null = True)
    First_Umpire_Id     = models.IntegerField()
    Second_Umpire_Id    = models.IntegerField()
    City_Name           = models.CharField(max_length = 100)
    Host_Country        = models.CharField(max_length = 100)

    def __str__(self) :
        return str(self.Match_Id)+' - '+ str(self.Match_Date)

class Team(models.Model):
    Team_Id         = models.IntegerField(primary_key=True, default = 0)
    Team_Name       = models.CharField(max_length = 100)
    Team_Short_Code = models.CharField(max_length = 100)

    def __str__(self) :
        return str(self.Team_Id)+' - '+self.Team_Name

class Player_Match(models.Model):
    Match_Id  = models.IntegerField(default = 0)
    Player_Id = models.IntegerField(default = 0)
    Team_Id   = models.IntegerField()
    Is_Keeper = models.IntegerField()
    Is_Captain = models.IntegerField()

    class Meta:
        unique_together = (('Match_Id', 'Player_Id'),)

    def __str__(self) :
        return str(self.Match_Id)+' - '+str(self.Player_Id)

class Ball_by_Ball(models.Model):
    Match_Id                = models.IntegerField(default = 0)
    Innings_Id              = models.IntegerField(default = 0)
    Over_Id                 = models.IntegerField(default = 0)
    Ball_Id                 = models.IntegerField(default = 0)
    Team_Batting_Id         = models.IntegerField()
    Team_Bowling_Id         = models.IntegerField()
    Striker_Id              = models.IntegerField()
    Striker_Batting_Position = models.IntegerField()
    Non_Striker_Id          = models.IntegerField()
    Bowler_Id               = models.IntegerField()
    Batsman_Scored          = models.IntegerField(null = True)
    Extra_Type              = models.CharField(max_length = 100, null = True)
    Extra_Runs              = models.IntegerField(null = True)
    Player_dissimal_Id      = models.IntegerField(null = True)
    Dissimal_Type           = models.CharField(max_length = 100, null = True)
    Fielder_Id              = models.IntegerField(null = True)

    class Meta:
        unique_together = (('Match_Id', 'Innings_Id','Over_Id','Ball_Id'),)

    def __str__(self) :
        return str(self.Match_Id) +' - '+ str(self.Innings_Id) + ' - ' + str(self.Over_Id) + ' - ' + str(self.Ball_Id)
