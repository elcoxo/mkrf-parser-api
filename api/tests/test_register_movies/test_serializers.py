import pytest

from register_movies.serializers import RegisterMovieSerializer
from tests.test_register_movies.conftest import movie_payloads

@pytest.mark.django_db
def test_serializer_valid_data(movie_payloads):
    serializer = RegisterMovieSerializer(data=movie_payloads["valid"])
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data["film_name"] == "Порко Россо"

@pytest.mark.django_db
def test_serializer_invalid_film_name(movie_payloads):
    serializer = RegisterMovieSerializer(data=movie_payloads["invalid_film_name"])
    assert not serializer.is_valid()
    assert "film_name" in serializer.errors