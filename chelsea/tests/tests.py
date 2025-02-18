from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from chelsea.models import Player, Manager, Competition, Season, Vote


class APITestCaseEndpoints(APITestCase):
    def setUp(self):
        """Set up initial test data."""
        self.player = Player.objects.create(name="Test Player")
        self.manager = Manager.objects.create(name="Test Manager")
        self.competition = Competition.objects.create(name="Test Competition")
        self.season = Season.objects.create(year=2023)

    def test_api_home(self):
        response = self.client.get(reverse('api_home'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_players(self):
        response = self.client.get(reverse('player-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_managers(self):
        response = self.client.get(reverse('manager-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_seasons(self):
        response = self.client.get(reverse('season-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_competitions(self):
        response = self.client.get(reverse('competition-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_player_by_name(self):
        response = self.client.get(reverse('get-player-by-name'), {'name': self.player.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_manager_by_name(self):
        response = self.client.get(reverse('get-manager-by-name'), {'name': self.manager.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cast_vote(self):
        response = self.client.post(reverse('cast-vote'), {'player_id': self.player.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_vote_comparison(self):
        response = self.client.get(reverse('vote-comparison'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_best_players(self):
        response = self.client.get(reverse('best-players'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_top_voted_player(self):
        response = self.client.get(reverse('top-voted-player'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_best_manager(self):
        response = self.client.get(reverse('best-manager'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_compare_players(self):
        response = self.client.get(reverse('compare-players'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_compare_managers(self):
        response = self.client.get(reverse('compare-managers'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_player_competition_stats(self):
        response = self.client.get(reverse('player-competition-stats', args=[self.player.id, self.competition.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_competition_stats(self):
        response = self.client.get(reverse('manager-competition-stats', args=[self.manager.id, self.competition.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
