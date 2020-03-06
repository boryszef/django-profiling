from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from api.models import Continent, Country


class ContinentSerializer(ModelSerializer):

    class Meta:
        model = Continent
        fields = '__all__'


class CountrySerializer(ModelSerializer):

    continent = SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Country
        fields = '__all__'
