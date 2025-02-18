from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    api_home, PlayerViewSet, ManagerViewSet, SeasonViewSet, CompetitionViewSet,
    CastVoteView, BestPlayersView, TopVotedPlayerView, BestManagerView,
    ComparePlayersView, CompareManagersView, VoteComparisonView, PlayerCompetitionStatsView, ManagerCompetitionStatsView
)

# Create a router and register the ViewSets
router = DefaultRouter()
router.register(r'players', PlayerViewSet, basename='player')
router.register(r'managers', ManagerViewSet, basename='manager')
router.register(r'seasons', SeasonViewSet, basename='season')
router.register(r'competitions', CompetitionViewSet, basename='competition')



urlpatterns = [
    path('', api_home, name="api_home"),  # API Welcome Message
    path('api/', include(router.urls)),  # Includes all ViewSets

    # Custom actions for getting player/manager by name
    path('api/players/get_by_name/', PlayerViewSet.as_view({'get': 'get_by_name'}), name='get-player-by-name'),
    path('api/managers/get_by_name/', ManagerViewSet.as_view({'get': 'get_by_name'}), name='get-manager-by-name'),

    # Voting System
    path('vote/', CastVoteView.as_view(), name='cast-vote'),
    path('vote/comparison/', VoteComparisonView.as_view(), name='vote-comparison'),

    # Voting & Leaderboard
    path('vote/', CastVoteView.as_view(), name='cast-vote'),
    path('leaderboard/best-players/', BestPlayersView.as_view(), name='best-players'),
    path('leaderboard/top-voted-player/', TopVotedPlayerView.as_view(), name='top-voted-player'),
    path('leaderboard/best-manager/', BestManagerView.as_view(), name='best-manager'),

    # Player & Manager Comparisons
    path("compare/players/", ComparePlayersView.as_view(), name="compare-players"),
    path("compare/managers/", CompareManagersView.as_view(), name="compare-managers"),

    # Retrieve Player & Manager Stats by Competition
    path("players/<int:player_id>/competition/<int:competition_id>/", PlayerCompetitionStatsView.as_view(), name="player-competition-stats"),
    path("managers/<int:manager_id>/competition/<int:competition_id>/", ManagerCompetitionStatsView.as_view(), name="manager-competition-stats"),
]
