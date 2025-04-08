from django.db import models
from datetime import date


class RegisterMovie(models.Model):
    id: int = models.IntegerField(primary_key=True, verbose_name='Идентификатор записи реестра')
    cardNumber: int = models.TextField(verbose_name='Номер удостоверения', null=True, blank=True)
    filmname: str = models.TextField(verbose_name='Название фильма')
    cardDate: date = models.DateField(verbose_name='Дата регистрации удостоверения', null=True, blank=True)
    director: str = models.TextField(verbose_name='Режиссер', null=True, blank=True)
    studio: str = models.TextField(verbose_name='Студия-производитель', null=True, blank=True)
    category: str = models.TextField(verbose_name='Категория', null=True, blank=True)
    viewMovie: str = models.TextField(verbose_name='Вид фильма', null=True, blank=True)
    color: str = models.TextField(verbose_name='Цвет', null=True, blank=True)
    ageCategory: str = models.TextField(verbose_name='Возрастная категория', null=True, blank=True)
    startDateRent: date = models.DateField(verbose_name='Дата начала показа фильма', null=True, blank=True)
    crYearOfProduction: date = models.DateField(verbose_name='Год производства', null=True, blank=True)
    countryOfProduction: str = models.TextField(verbose_name='Страна производства', null=True, blank=True)

    class Meta:
        db_table = "register_movies_db"