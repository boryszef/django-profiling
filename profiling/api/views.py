from rest_framework.generics import ListAPIView

from api.models import Continent, Country, Airport, City, Currency
from api.serializers import ContinentSerializer, CountrySerializer, AirportSerializer, CitySerializer, \
    CurrencySerializer


class ContinentView(ListAPIView):

    queryset = Continent.objects.all()
    serializer_class = ContinentSerializer


class CountryView(ListAPIView):

    queryset = Country.objects.select_related(
        'continent'
    ).prefetch_related(
        'currency_set'
    ).all()
    serializer_class = CountrySerializer


class AirportView(ListAPIView):

    queryset = Airport.objects.select_related('continent', 'country').all()
    serializer_class = AirportSerializer


class CityView(ListAPIView):
    queryset = City.objects.select_related('country').all()
    serializer_class = CitySerializer


class CurrencyView(ListAPIView):
    queryset = Currency.objects.select_related('country').all()
    serializer_class = CurrencySerializer
