from django.contrib.postgres.fields import ArrayField
from django.db import models


class Continent(models.Model):
    code = models.CharField(max_length=2, primary_key=True, verbose_name='Code')
    name = models.TextField(null=False, verbose_name='Name')


class Country(models.Model):
    alpha2 = models.CharField(max_length=2, unique=True, primary_key=True, verbose_name='ISO3166-1-Alpha-2')
    alpha3 = models.CharField(max_length=3, unique=True, verbose_name='ISO3166-1-Alpha-3')
    dial = models.TextField(verbose_name='Dial')
    name = models.TextField(verbose_name='UNTERM English Formal')
    capital = models.TextField(verbose_name='Capital')
    continent = models.ForeignKey(Continent, null=True, on_delete=models.CASCADE, verbose_name='Continent')
    ds = models.CharField(max_length=3, verbose_name='DS')
    languages = ArrayField(base_field=models.TextField(), default=list, verbose_name='Languages')


class Airport(models.Model):
    ident = models.CharField(max_length=8, primary_key=True, verbose_name='ident')
    type = models.TextField(verbose_name='type')
    name = models.TextField(verbose_name='name')
    elevation = models.FloatField(verbose_name='elevation_ft', null=True)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE, verbose_name='continent')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='iso_country', null=True)
    gps_code = models.CharField(max_length=4, verbose_name='gps_code')
    iata_code = models.CharField(max_length=3, verbose_name='iata_code')
    latitude = models.FloatField(verbose_name='coordinates')
    longitude = models.FloatField(verbose_name='coordinates')
