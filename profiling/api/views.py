from rest_framework.generics import ListAPIView

from api.models import Continent, Country, Airport, City
from api.serializers import ContinentSerializer, CountrySerializer, AirportSerializer, CitySerializer


class ContinentView(ListAPIView):

    queryset = Continent.objects.all()
    serializer_class = ContinentSerializer


class CountryView(ListAPIView):

    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class AirportView(ListAPIView):

    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class CityView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
