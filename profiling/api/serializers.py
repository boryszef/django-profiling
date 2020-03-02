from rest_framework.serializers import ModelSerializer

from api.models import Title


class TitleSerializer(ModelSerializer):

    class Meta:
        model = Title
        fields = '__all__'
