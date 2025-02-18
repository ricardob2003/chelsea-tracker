from rest_framework import serializers
from ..models import Player, Manager, Season, Competition

# ==============================
# 📌 MANAGER SERIALIZER
# ==============================
class ManagerSerializer(serializers.ModelSerializer):
    win_rate = serializers.ReadOnlyField()
    vote_count = serializers.SerializerMethodField()

    class Meta:
        model = Manager
        fields = '__all__'

    @staticmethod
    def validate_start_year(value):
        if value < 1900:
            raise serializers.ValidationError("Start year must be realistic.")
        return value

    def get_vote_count(self, obj):
        return obj.votes.count()

    def validate(self, data):
        start_year = data.get("start_year")
        end_year = data.get("end_year")
        if end_year and end_year < start_year:
            raise serializers.ValidationError("End year cannot be before start year.")
        return data


# ==============================
# 📌 PLAYER SERIALIZER
# ==============================
class PlayerSerializer(serializers.ModelSerializer):
    vote_count = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = '__all__'

    def get_vote_count(self, obj):
        return obj.votes.count()

    @staticmethod
    def validate_age(value):
        if not (15 <= value <= 50):
            raise serializers.ValidationError("Age must be between 15 and 50.")
        return value

    @staticmethod
    def validate_position(value):
        allowed_positions = ["GK", "DEF", "MID", "FWD"]
        if value not in allowed_positions:
            raise serializers.ValidationError(f"Invalid position '{value}'. Allowed: {allowed_positions}")
        return value

    def validate(self, data):
        start_year = data.get("start_year")
        end_year = data.get("end_year")
        if end_year and end_year < start_year:
            raise serializers.ValidationError("End year cannot be before start year.")
        return data


# ==============================
# 📌 SEASON SERIALIZER
# ==============================
class SeasonSerializer(serializers.ModelSerializer):
    player = serializers.StringRelatedField()
    manager = serializers.StringRelatedField()
    competition = serializers.SlugRelatedField(slug_field="name", queryset=Competition.objects.all())

    class Meta:
        model = Season
        fields = '__all__'

    @staticmethod
    def validate_year(value):
        import re
        if not re.match(r"^\d{4}/\d{2}$", value):
            raise serializers.ValidationError("Year must be in the format YYYY/YY (e.g., 2015/16).")
        return value


# ==============================
# 📌 COMPETITION SERIALIZER
# ==============================
class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = '__all__'
