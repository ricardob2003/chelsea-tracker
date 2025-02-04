from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

# Import all models dynamically to avoid hardcoding
from ..models import *  # Ensures all models are available without manual imports

# Import all serializers dynamically
from .serializers import *  # Ensures new serializers are automatically included


### API Home ###
def api_home(request, *args, **kwargs):
    return JsonResponse({"message": "Welcome to Chelsea Tracker API!"})


### Player ViewSet ###
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


### Manager ViewSet ###
class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer


### Season ViewSet ###
class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer


### Competition ViewSet ###
class CompetitionViewSet(viewsets.ModelViewSet):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
