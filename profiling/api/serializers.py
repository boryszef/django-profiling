from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from api.models import Continent, Country, Airport, City


class ContinentSerializer(ModelSerializer):

    class Meta:
        model = Continent
        fields = '__all__'


class CountrySerializer(ModelSerializer):

    continent = SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Country
        fields = '__all__'


class AirportSerializer(ModelSerializer):

    continent = SlugRelatedField(slug_field='name', read_only=True)
    country = SlugRelatedField(slug_field='official_name', read_only=True)

    class Meta:
        model = Airport
        fields = '__all__'


class CitySerializer(ModelSerializer):

    country = SlugRelatedField(slug_field='official_name', read_only=True)

    class Meta:
        model = City
        fields = '__all__'
