from django.urls import path

from api.register_movies.apps import RegisterMoviesConfig
from api.register_movies.views import RegisterMoviesListAPIView

app_name = RegisterMoviesConfig.name

urlpatterns = [
    path('register_movies', RegisterMoviesListAPIView.as_view(), name='Get List of Registered Movies'),
]