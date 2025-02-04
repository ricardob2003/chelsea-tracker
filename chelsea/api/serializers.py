from rest_framework import serializers
from ..models import *  # Import all models from models.py

### Manager Serializer ###
class ManagerSerializer(serializers.ModelSerializer):
    win_rate = serializers.ReadOnlyField()  # Calculated property, read-only

    class Meta:
        model = Manager
        fields = '__all__'

    def validate_start_year(self, value):
        if value < 1900:  # Basic validation
            raise serializers.ValidationError("Start year must be realistic.")
        return value

    def validate(self, data):
        """Ensure end_year is after start_year if provided."""
        start_year = data.get("start_year")
        end_year = data.get("end_year")
        if end_year and end_year < start_year:
            raise serializers.ValidationError("End year cannot be before start year.")
        return data


### Player Serializer ###
class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

    def validate_age(self, value):
        """Ensure age is within a reasonable range."""
        if not (15 <= value <= 50):  # Assuming a reasonable age range for footballers
            raise serializers.ValidationError("Age must be between 15 and 50.")
        return value

    def validate(self, data):
        """Ensure end_year is after start_year if provided."""
        start_year = data.get("start_year")
        end_year = data.get("end_year")
        if end_year and end_year < start_year:
            raise serializers.ValidationError("End year cannot be before start year.")
        return data


### Season Serializer ###
class SeasonSerializer(serializers.ModelSerializer):
    player = serializers.StringRelatedField()
    manager = serializers.StringRelatedField()
    competition = serializers.SlugRelatedField(slug_field="name", queryset=Competition.objects.all())

    class Meta:
        model = Season
        fields = '__all__'

    def validate_year(self, value):
        """Ensure the year format is correct."""
        import re
        if not re.match(r"^\d{4}/\d{2}$", value):  # E.g., "2015/16"
            raise serializers.ValidationError("Year must be in the format YYYY/YY (e.g., 2015/16).")
        return value


### Competition Serializer ###
class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = '__all__'


### Vote Serializer ###
class VoteSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)  # Nested for better response
    manager = ManagerSerializer(read_only=True)

    class Meta:
        model = Vote
        fields = '__all__'

    def validate(self, data):
        """Ensure either player or manager is provided, but not both."""
        if not data.get("player") and not data.get("manager"):
            raise serializers.ValidationError("Vote must be for either a player or a manager.")
        if data.get("player") and data.get("manager"):
            raise serializers.ValidationError("Vote cannot be for both a player and a manager.")
        return data
