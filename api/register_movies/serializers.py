from rest_framework import serializers
from .models import RegisterMovie

class RegisterMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterMovie
        fields = (
            'id',
            'registry_id',
            'card_number',
            'film_name',
            'card_date',
            'director',
            'studio',
            'category',
            'view_movie',
            'color',
            'age_category',
            'start_date_rent',
            'year_of_production',
            'country_of_production',
        )

    read_only_fields = 'id'

    def validate_film_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Film name cannot be empty.")
        return value