from rest_framework import serializers
from .models import RegisterMovie

class RegisterMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterMovie
        fields = (
            'cardNumber',
            'filmname',
            'cardDate',
            'director',
            'studio',
            'category',
            'viewMovie',
            'color',
            'ageCategory',
            'startDateRent',
            'crYearOfProduction',
            'countryOfProduction',
        )
