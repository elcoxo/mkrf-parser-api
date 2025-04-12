from django.db import models
from datetime import date

class RegisterMovie(models.Model):
    registry_id: int = models.PositiveIntegerField(verbose_name='Идентификатор записи реестра')
    card_number: int = models.PositiveIntegerField(verbose_name='Номер удостоверения', null=True, blank=True)
    film_name: str = models.TextField(verbose_name='Название фильма')
    card_date: date = models.DateField(verbose_name='Дата регистрации удостоверения', null=True, blank=True)
    director: str = models.TextField(verbose_name='Режиссер', null=True, blank=True)
    studio: str = models.TextField(verbose_name='Студия-производитель', null=True, blank=True)
    category: str = models.CharField(max_length=100, verbose_name='Категория', null=True, blank=True)
    view_movie: str = models.CharField(max_length=100, verbose_name='Вид фильма', null=True, blank=True)
    color: str = models.CharField(max_length=100, verbose_name='Цвет', null=True, blank=True)
    age_category: str = models.TextField(verbose_name='Возрастная категория', null=True, blank=True)
    start_date_rent: date = models.DateField(verbose_name='Дата начала показа фильма', null=True, blank=True)
    year_of_production: int = models.PositiveIntegerField(verbose_name='Год производства', null=True, blank=True)
    country_of_production: str = models.CharField(max_length=100, verbose_name='Страна производства', null=True, blank=True)

    class Meta:
        db_table = "register_movies"

