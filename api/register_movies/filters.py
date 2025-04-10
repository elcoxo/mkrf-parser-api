import django_filters
from api.register_movies.models import RegisterMovie

class RegisterMovieFilter(django_filters.FilterSet):
    class Meta:
        model = RegisterMovie
        fields = {
            'registry_id': ['exact'],
            'card_number': ['exact'],
            'film_name': ['iexact', 'icontains'],
            'card_date': ['exact', 'lt', 'gt', 'range'],
            'director': ['iexact', 'icontains'],
            'studio': ['iexact', 'icontains'],
            'category': ['iexact', 'icontains'],
            'view_movie': ['iexact', 'icontains'],
            'color': ['iexact', 'icontains'],
            'age_category': ['iexact', 'icontains'],
            'start_date_rent': ['exact', 'lt', 'gt', 'range'],
            'year_of_production': ['exact'],
            'country_of_production': ['iexact', 'icontains'],
        }