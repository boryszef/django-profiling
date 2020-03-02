from django.urls import path

from api.views import TitleView


app_name = 'api'

urlpatterns = [
    path('titles/', TitleView.as_view())
]
