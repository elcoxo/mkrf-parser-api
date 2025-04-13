import pytest

from tests.test_register_movies.conftest import movie_payloads, client
from tests.test_register_movies.factories import RegisterMovieFactory

@pytest.mark.django_db
def test_register_movie_list(client):
    RegisterMovieFactory.create_batch(10)
    response = client.get("/api/v1/register_movies")

    assert response.status_code == 200
    assert response.json()["count"] == 10


@pytest.mark.django_db
def test_register_movie_post(client, movie_payloads):
    response = client.post("/api/v1/register_movies", movie_payloads["valid"], format="json")
    assert response.status_code == 201
    assert response.json()["film_name"] == "Порко Россо"

