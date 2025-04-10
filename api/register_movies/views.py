from drf_spectacular.utils import extend_schema
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters, status, generics
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User

from api.register_movies.filters import RegisterMovieFilter
from api.register_movies.models import RegisterMovie
from api.register_movies.serializers import RegisterMovieSerializer


class RegisterMoviesPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_query_param = 'page'
    page_size_query_param = 'size'

class RegisterMoviesListAPIView(generics.ListCreateAPIView):
    """
    View to list all registered movies (GET) and create a new movie (POST).
    """
    queryset = RegisterMovie.objects.order_by('pk')
    serializer_class = RegisterMovieSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['registry_id', 'card_number', 'film_name', 'director', 'studio',
                     'category', 'view_movie', 'color', 'age_category', 'country_of_production']

    pagination_class = RegisterMoviesPagination

