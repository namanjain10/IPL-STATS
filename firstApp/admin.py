from django.contrib import admin
from firstApp.models import Player, Season, Player_Match, Match, Ball_by_Ball, Team

# Register your models here.
admin.site.register (Player)
admin.site.register (Season)
admin.site.register (Player_Match)
admin.site.register (Match)
admin.site.register (Ball_by_Ball)
admin.site.register (Team)
