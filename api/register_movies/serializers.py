from rest_framework import serializers
from api.register_movies.models import RegisterMovie

class RegisterMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterMovie
        fields = (
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
