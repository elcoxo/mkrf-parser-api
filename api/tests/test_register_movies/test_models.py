import pytest

from register_movies.models import RegisterMovie


@pytest.mark.django_db
def test_register_movie_create(movie_payloads):
    movie = RegisterMovie.objects.create(**movie_payloads['valid'])

    assert movie.registry_id == 11543917
    assert movie.film_name == "Порко Россо"
    assert movie.card_date == '2025-04-01'
    assert movie.year_of_production == 1992


@pytest.mark.django_db
def test_register_movie_create_minimal(movie_payloads):
    movie = RegisterMovie.objects.create(**movie_payloads['minimal'])
    assert movie.card_number is None
    assert movie.director is None
    assert movie.card_date is None
