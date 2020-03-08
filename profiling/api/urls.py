from django.urls import path

from api.views import ContinentView, CountryView, AirportView, CityView

app_name = 'api'

urlpatterns = [
    path('continents/', ContinentView.as_view()),
    path('countries/', CountryView.as_view()),
    path('airports/', AirportView.as_view()),
    path('cities/', CityView.as_view()),
]
