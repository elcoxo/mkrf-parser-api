from rest_framework.pagination import PageNumberPagination

from rest_framework import filters, generics

from api.register_movies.models import RegisterMovie
from api.register_movies.serializers import RegisterMovieSerializer

class RegisterMoviesListAPIView(generics.ListCreateAPIView):
    """
    View to list all registered movies (GET) and create a new movie (POST).
    """
    queryset = RegisterMovie.objects.order_by('pk')
    serializer_class = RegisterMovieSerializer

