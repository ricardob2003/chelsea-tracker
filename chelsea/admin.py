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
    list_display = ("id", "player", "manager", "vote_count", "timestamp")

    @admin.display(description="Votes Count")
    def vote_count(self, obj):
        """
        Count the number of votes for each player/manager dynamically.
        """
        if obj.player:
            return Vote.objects.filter(player=obj.player).count()
        elif obj.manager:
            return Vote.objects.filter(manager=obj.manager).count()
        return 0