from rest_framework.generics import ListAPIView

from api.models import Continent, Country
from api.serializers import ContinentSerializer, CountrySerializer


class ContinentView(ListAPIView):

    queryset = Continent.objects.all()
    serializer_class = ContinentSerializer


class CountryView(ListAPIView):

    queryset = Country.objects.all()
    serializer_class = CountrySerializer
