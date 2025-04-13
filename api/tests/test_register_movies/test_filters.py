import pytest

from .factories import RegisterMovieFactory

@pytest.mark.django_db
def test_register_movie_list_search(client):
    RegisterMovieFactory(film_name="Порко Россо")
    RegisterMovieFactory(director="порко галлиард")
    RegisterMovieFactory(film_name="Россошь")

    response = client.get("/api/v1/register_movies?search=порко")
    results = response.json()["results"]
    film_names = [result["film_name"] for result in results]
    director_names = [result["director"] for result in results]

    assert response.status_code == 200
    assert len(results) == 2
    assert "Порко Россо" in film_names
    assert "порко галлиард" in director_names

@pytest.mark.django_db
def test_search_with_pagination(client):
    RegisterMovieFactory.create_batch(15, film_name="Порко Россо")
    response = client.get("/api/v1/register_movies?search=порко&size=10")
    assert len(response.json()["results"]) == 10, {response.content}
    assert response.json()["count"] == 15