from django.contrib import admin
from .models import Manager, Player, Season, Competition, Vote

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_year', 'end_year', 'win_rate', 'actual_points')
    search_fields = ('name',)
    list_filter = ('start_year', 'end_year')
    readonly_fields = ('win_rate',)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'nationality', 'age', 'start_year', 'end_year')
    search_fields = ('name', 'nationality')
    list_filter = ('position', 'start_year', 'end_year')


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('player', 'year', 'competition', 'goals', 'assists', 'matches', 'minutes_played')
    search_fields = ('player__name', 'competition__name', 'year')
    list_filter = ('year', 'competition')


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation')
    search_fields = ('name', 'abbreviation')


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('player', 'manager', 'votes_count', 'timestamp')
    search_fields = ('player__name', 'manager__name')
    list_filter = ('timestamp',)