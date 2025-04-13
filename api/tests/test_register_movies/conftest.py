import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def movie_payloads():
    return {
        "valid": {
            "registry_id": 11543917,
            "card_number": 124003225,
            "film_name": "Порко Россо",
            "card_date": "2025-04-01",
            "director": "Хаяо Миядзаки",
            "studio": "Джэпэн Эйрлайнс, Нибарики, Ниппон Телевижн, Студио Гибли",
            "category": "Кино",
            "view_movie": "Анимационный",
            "color": "Цветной",
            "age_category": "«16+» для детей старше 16 лет",
            "start_date_rent": "2025-04-09",
            "year_of_production": 1992,
            "country_of_production": "Япония"
        },
        "invalid_film_name": {
            "registry_id": 2,
            "film_name": "",
            "year_of_production": 2022
        },
        "partial_update": {
            "film_name": "Updated Movie",
            "director": "Jane Doe"
        },
        "minimal": {
            "registry_id": 3,
            "film_name": "Minimal Movie"
        }
    }
