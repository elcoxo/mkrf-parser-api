import math

from rest_framework.pagination import PageNumberPagination
from rest_framework import filters, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from .filters import RegisterMovieFilter
from .models import RegisterMovie
from .serializers import RegisterMovieSerializer


class RegisterMoviesPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_query_param = 'page'
    page_size_query_param = 'size'

    def get_paginated_response(self, data):
        total_count = self.page.paginator.count
        page_size = self.get_page_size(self.request)
        last_page = math.ceil(total_count / page_size) if page_size else 1

        return Response({
            'links': {
                'current': self.page.number,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'last': last_page,
            },
            'count': total_count,
            'countItemsOnPage': page_size,
            'results': data
        })


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
