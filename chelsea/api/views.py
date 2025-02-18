from django.db.models import Count
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

from ..models import Player, Manager, Season, Competition, Vote
from .serializers import PlayerSerializer, ManagerSerializer, SeasonSerializer, CompetitionSerializer


### 📌 API Home ###
def api_home(request, *args, **kwargs):
    return JsonResponse({"message": "Welcome to Chelsea Tracker API!"})


### 📌 Player ViewSet ###
class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    @action(detail=False, methods=['get'])
    def get_by_name(self, request):
        """
        Retrieve a player by name.
        Example: /api/players/get_by_name/?name=Eden Hazard
        """
        name = request.GET.get('name')
        if not name:
            return JsonResponse({"error": "Name parameter is required."}, status=400)

        try:
            player = Player.objects.get(name__iexact=name)  # Case-insensitive match
            serializer = PlayerSerializer(player)
            return JsonResponse(serializer.data, safe=False)
        except Player.DoesNotExist:
            return JsonResponse({"error": "Player not found."}, status=404)


### 📌 Manager ViewSet ###
class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer


### 📌 Season ViewSet ###
class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer


### 📌 Competition ViewSet ###
class CompetitionViewSet(viewsets.ModelViewSet):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer


# ==============================
# 🗳️ VOTING SYSTEM
# ==============================
class CastVoteView(APIView):
    """
    API to cast a vote for a player or manager.
    """

    def post(self, request, *args, **kwargs):
        player_id = request.data.get("player_id")
        manager_id = request.data.get("manager_id")

        if not player_id and not manager_id:
            return Response(
                {"error": "A vote must be cast for either a player or a manager."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if player_id and manager_id:
            return Response(
                {"error": "A vote cannot be cast for both a player and a manager at the same time."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            if player_id:
                player = Player.objects.get(id=player_id)
                Vote.objects.create(player=player)

            elif manager_id:
                manager = Manager.objects.get(id=manager_id)
                Vote.objects.create(manager=manager)

        except (Player.DoesNotExist, Manager.DoesNotExist):
            return Response(
                {"error": "Player or Manager not found."}, status=status.HTTP_404_NOT_FOUND
            )

        return Response({"message": "Vote cast successfully!"}, status=status.HTTP_201_CREATED)


class VoteComparisonView(APIView):
    """
    API to cast a vote for a player comparison based on all-time stats.
    Only allows voting if both players play in the same position.
    """

    def post(self, request, *args, **kwargs):
        player1_id = request.data.get("player1_id")
        player2_id = request.data.get("player2_id")

        if not player1_id or not player2_id:
            return Response(
                {"error": "Both player1_id and player2_id are required for voting."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            player1 = Player.objects.get(id=player1_id)
            player2 = Player.objects.get(id=player2_id)

            if player1.position != player2.position:
                return Response(
                    {"error": "Players must be in the same position to be compared."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            voted_player_id = request.data.get("vote_for")  # The player user voted for

            if voted_player_id not in [player1.id, player2.id]:
                return Response(
                    {"error": "vote_for must be one of the compared players."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            voted_player = Player.objects.get(id=voted_player_id)
            Vote.objects.create(player=voted_player)

            return Response({"message": "Vote cast successfully!"}, status=status.HTTP_201_CREATED)

        except Player.DoesNotExist:
            return Response({"error": "One or both players not found."}, status=status.HTTP_404_NOT_FOUND)


# ==============================
# 🏆 LEADERBOARD & BEST PLAYER/MANAGER
# ==============================
class BestPlayersView(APIView):
    """
    Retrieve the best 11 players following a structured formation.
    """

    def get(self, request, *args, **kwargs):
        POSITIONS = {
            "Keeper": 1,  # 1 Goalkeeper
            "Defense": 4,  # 4 Defenders
            "Midfield": 3,  # 3 Midfielders
            "Forward": 3  # 3 Attackers
        }

        players = Player.objects.annotate(vote_count=Count("votes")).order_by("-vote_count")
        best_11 = []

        for category, limit in POSITIONS.items():
            best_11.extend(players.filter(position=category)[:limit])

        serializer = PlayerSerializer(best_11, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TopVotedPlayerView(APIView):
    """
    Retrieve the player with the most votes.
    """

    def get(self, request):
        top_player = Player.objects.annotate(vote_count=Count('votes')).order_by('-vote_count').first()
        if not top_player:
            return Response({"error": "No votes registered yet."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlayerSerializer(top_player)
        return Response(serializer.data)


class BestManagerView(APIView):
    """
    Retrieve the manager with the most votes.
    """

    def get(self, request, *args, **kwargs):
        best_manager = Manager.objects.annotate(vote_count=Count("votes")).order_by("-vote_count").first()
        if not best_manager:
            return Response({"error": "No votes found for managers."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ManagerSerializer(best_manager)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ==============================
# ⚖️ PLAYER & MANAGER COMPARISON
# ==============================
class ComparePlayersView(APIView):
    """
    Compare two players based on their stats in a specific competition.
    """

    def get(self, request, *args, **kwargs):
        player1_id = request.GET.get("player1_id")
        player2_id = request.GET.get("player2_id")
        competition_id = request.GET.get("competition_id")

        if not player1_id or not player2_id or not competition_id:
            return Response({"error": "player1_id, player2_id, and competition_id are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            player1 = Player.objects.get(id=player1_id)
            player2 = Player.objects.get(id=player2_id)
            competition = Competition.objects.get(id=competition_id)

            return Response({
                "player1": PlayerSerializer(player1).data,
                "player2": PlayerSerializer(player2).data
            }, status=status.HTTP_200_OK)

        except (Player.DoesNotExist, Competition.DoesNotExist):
            return Response({"error": "Player or competition not found."}, status=status.HTTP_404_NOT_FOUND)


class CompareManagersView(APIView):
    """
    Compare two managers.
    """

    def get(self, request, *args, **kwargs):
        manager1_id = request.GET.get("manager1_id")
        manager2_id = request.GET.get("manager2_id")

        if not manager1_id or not manager2_id:
            return Response({"error": "Both manager IDs are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            manager1 = Manager.objects.get(id=manager1_id)
            manager2 = Manager.objects.get(id=manager2_id)

            return Response({
                "manager1": ManagerSerializer(manager1).data,
                "manager2": ManagerSerializer(manager2).data
            }, status=status.HTTP_200_OK)

        except Manager.DoesNotExist:
            return Response({"error": "One or both managers not found."}, status=status.HTTP_404_NOT_FOUND)


class PlayerCompetitionStatsView(APIView):
    """
    Retrieve player stats for a specific competition.
    """

    def get(self, request, player_id, competition_id, *args, **kwargs):
        try:
            player = Player.objects.get(id=player_id)
            competition = Competition.objects.get(id=competition_id)
            stats = Season.objects.filter(player=player, competition=competition).first()

            if not stats:
                return Response({"error": "No stats found for this player in this competition."},
                                status=status.HTTP_404_NOT_FOUND)

            return Response({
                "player": PlayerSerializer(player).data,
                "competition": competition.name
            }, status=status.HTTP_200_OK)

        except (Player.DoesNotExist, Competition.DoesNotExist):
            return Response({"error": "Player or Competition not found."}, status=status.HTTP_404_NOT_FOUND)


class ManagerCompetitionStatsView(APIView):
    """
    Retrieve manager stats for a specific competition.
    Example: GET /managers/1/competition/5/
    """

    def get(self, request, manager_id, competition_id, *args, **kwargs):
        try:
            manager = Manager.objects.get(id=manager_id)
            competition = Competition.objects.get(id=competition_id)

            # Fetch the stats for the manager in the specified competition
            stats = Season.objects.filter(manager=manager, competition=competition).first()

            if not stats:
                return Response(
                    {"error": "No stats found for this manager in this competition."},
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response({
                "manager": ManagerSerializer(manager).data,
                "competition": competition.name,
                "stats": {
                    "matches": stats.matches,
                    "wins": stats.wins,
                    "draws": stats.draws,
                    "losses": stats.losses,
                    "points": stats.points
                }
            }, status=status.HTTP_200_OK)

        except (Manager.DoesNotExist, Competition.DoesNotExist):
            return Response(
                {"error": "Manager or Competition not found."},
                status=status.HTTP_404_NOT_FOUND
            )
