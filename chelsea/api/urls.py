from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import api_home, PlayerViewSet, ManagerViewSet, SeasonViewSet, CompetitionViewSet

# Create a router and register the ViewSets
router = DefaultRouter()
router.register(r'players', PlayerViewSet, basename='player')
router.register(r'managers', ManagerViewSet, basename='manager')
router.register(r'seasons', SeasonViewSet, basename='season')
router.register(r'competitions', CompetitionViewSet, basename='competition')

urlpatterns = [
    path('', api_home, name="api_home"),  # API Welcome Message
    path('api/', include(router.urls)),  # Includes all ViewSets for the Chelsea app
    path('api/players/get_by_name/', PlayerViewSet.as_view({'get': 'get_by_name'})),  # Custom player search by name
]