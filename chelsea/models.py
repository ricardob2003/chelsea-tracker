from django.db import models


class Manager(models.Model):
    name = models.CharField(max_length=100)
    start_year = models.IntegerField()  # Year the manager started at Chelsea
    end_year = models.IntegerField(null=True, blank=True)  # Year the manager left Chelsea (null if still at Chelsea)
    preferred_formation = models.CharField(max_length=50, null=True, blank=True)  # E.g., "4-3-3", "3-4-3"
    trophies_won = models.IntegerField(default=0)

    # Record of games
    games_won = models.IntegerField(default=0)
    games_drawn = models.IntegerField(default=0)
    games_lost = models.IntegerField(default=0)

    # Points
    expected_points = models.FloatField(default=0.0)
    actual_points = models.FloatField(default=0.0)

    # Big wins and losses
    biggest_win = models.CharField(max_length=100, null=True, blank=True)  # E.g., "6-0 vs Arsenal (2021)"
    biggest_loss = models.CharField(max_length=100, null=True, blank=True)  # E.g., "0-4 vs Man Utd (2020)"


    def __str__(self):
        return self.name

    @property
    def win_rate(self):
        total_games = self.games_won + self.games_drawn + self.games_lost
        return (self.games_won / total_games) * 100 if total_games > 0 else 0


class Player(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Ensures no duplicate players
    position = models.CharField(max_length=50)  # E.g., Winger, Forward
    nationality = models.CharField(max_length=50)
    age = models.IntegerField()
    start_year = models.IntegerField()  # Year the player joined Chelsea
    end_year = models.IntegerField(null=True, blank=True)
    take_ons = models.CharField(default=0 ,max_length=10)  # Store as "2/2" or "4/4"
    aerial_duels_won = models.CharField(default=0, max_length=10)
    photo_url = models.URLField(blank=True, null=True)# Year the player left Chelsea (null if still at Chelsea)
    POSITION_CHOICES = [
        ("GK", "Goalkeeper"),
        ("DEF", "Defender"),
        ("MID", "Midfielder"),
        ("FWD", "Forward"),
    ]
    def __str__(self):
        return self.name


class Season(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="seasons")
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name="seasons", null=True, blank=True)
    competition = models.ForeignKey('Competition', on_delete=models.CASCADE, related_name="seasons")
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    matches = models.IntegerField(default=0)
    minutes_played = models.IntegerField(default=0)
    year = models.CharField(max_length=9)  # E.g., "2015/16"

    tackles = models.IntegerField(default=0)
    recoveries = models.IntegerField(default=0)
    ground_duels_won_pct = models.FloatField(default=0)

    def __str__(self):
        return f"{self.player.name} - {self.year} ({self.competition.name})"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['player', 'competition', 'year'],
                name='unique_season_per_player_and_competition'
            )
        ]


class Competition(models.Model):
    name = models.CharField(max_length=100)  # E.g., "Premier League", "FA Cup"
    description = models.TextField(null=True, blank=True)
    abbreviation = models.CharField(max_length=10, null=True, blank=True)  # E.g., "PL", "FAC"

    def __str__(self):
        return self.name


class Vote(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="votes", null=True, blank=True)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name="votes", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)  # Tracks when the vote was cast

    def __str__(self):
        if self.player:
            return f"Vote for {self.player.name}"
        elif self.manager:
            return f"Vote for {self.manager.name}"
        return "Unspecified vote"

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(player__isnull=False, manager__isnull=True) |
                    models.Q(player__isnull=True, manager__isnull=False)
                ),
                name="only_one_of_player_or_manager",
            )
        ]
