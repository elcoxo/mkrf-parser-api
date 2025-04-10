from rest_framework.pagination import PageNumberPagination

from rest_framework import filters, generics
from django_filters.rest_framework import DjangoFilterBackend

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
    View to list all registered movies.

    GET: Get all registered movies.
    POST: Create a new movie.
    """
    queryset = RegisterMovie.objects.order_by('pk')
    serializer_class = RegisterMovieSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = RegisterMovieFilter
    search_fields = ['registry_id', 'card_number', 'film_name', 'director', 'studio',
                     'category', 'view_movie', 'color', 'age_category', 'country_of_production']
    ordering_fields = '__all__'

    pagination_class = RegisterMoviesPagination

class RegisterMovieDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to single registered movie by primary key.

    GET: Get single movie details.
    PATCH: Update movie details.
    DELETE: Delete the movie.
    """
    queryset = RegisterMovie.objects.all()
    serializer_class = RegisterMovieSerializer
    http_method_names = ['get', 'patch', 'delete']

