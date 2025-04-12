from django.urls import path

from .apps import RegisterMoviesConfig
from .views import RegisterMoviesListAPIView, RegisterMovieDetailAPIView

app_name = RegisterMoviesConfig.name

urlpatterns = [
    path('register_movies', RegisterMoviesListAPIView.as_view(), name='register-movie-list'),
    path('register_movies/<int:pk>/', RegisterMovieDetailAPIView.as_view(), name='register-movie-detail'),
]
