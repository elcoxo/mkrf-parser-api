import factory
from datetime import date
from register_movies.models import RegisterMovie

class RegisterMovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RegisterMovie

    registry_id = factory.Faker("random_int", min=1, max=10000)
    card_number = factory.Faker("random_int", min=1, max=10000)
    film_name = factory.Faker("sentence", nb_words=4)
    card_date = factory.Faker("date_this_decade")
    director = factory.Faker("name")
    studio = factory.Faker("company")
    category = factory.Faker("word")
    view_movie = factory.Faker("word")
    color = factory.Faker("color_name")
    age_category = factory.Faker("random_element", elements=("6+", "12+", "16+", "18+"))
    start_date_rent = factory.Faker("date_this_year")
    year_of_production = factory.Faker("random_int", min=1900, max=2025)
    country_of_production = factory.Faker("country")