from rest_framework.generics import ListAPIView

from api.models import Title
from api.serializers import TitleSerializer


class TitleView(ListAPIView):

    queryset = Title.objects.all()[:100]
    serializer_class = TitleSerializer
