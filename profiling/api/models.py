from django.contrib.postgres.fields import ArrayField
from django.db import models


class Continent(models.Model):
    code = models.CharField(max_length=2, primary_key=True, verbose_name='Code')
    name = models.TextField(null=False, verbose_name='Name')


class Country(models.Model):
    alpha2 = models.CharField(
        max_length=2,
        unique=True,
        primary_key=True,
        verbose_name='ISO3166-1-Alpha-2',
        help_text='Alpha-2 codes from ISO 3166-1'
    )
    alpha3 = models.CharField(
        max_length=3,
        unique=True,
        verbose_name='ISO3166-1-Alpha-3',
        help_text='Alpha-3 codes from ISO 3166-1 (synonymous with World Bank Codes)'
    )
    dial = models.TextField(
        verbose_name='Dial',
        help_text='Country code from ITU-T recommendation E.164, sometimes followed by area code'
    )
    formal_name = models.TextField(
        verbose_name='UNTERM English Formal',
        help_text='Country\'s formal English name from UN Protocol and Liaison Service'
    )
    official_name = models.TextField(
        verbose_name='official_name_en',
        help_text='Country or Area official English short name from UN Statistics Divsion'
    )
    short_name = models.TextField(
        verbose_name='UNTERM English Short',
        help_text='Country\'s short English name from UN Protocol and Liaison Service'
    )
    capital = models.TextField(
        verbose_name='Capital',
        help_text='Capital city from Geonames'
    )
    continent = models.ForeignKey(
        Continent,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Continent',
        help_text='Continent from Geonames'
    )
    ds = models.CharField(
        max_length=3,
        verbose_name='DS',
        help_text='Distinguishing signs of vehicles in international traffic'
    )
    languages = ArrayField(
        base_field=models.TextField(),
        default=list,
        verbose_name='Languages',
        help_text='Languages from Geonames'
    )


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


class City(models.Model):
    name = models.TextField(verbose_name='name')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, verbose_name='country')
    subcountry = models.TextField(verbose_name='subcountry')


class Currency(models.Model):
    name = models.TextField(verbose_name='Currency')
    code = models.CharField(max_length=3, verbose_name='AlphabeticCode')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, verbose_name='Entity')
    withdrawal_date = models.DateField(null=True, verbose_name='WithdrawalDate')

    def __str__(self):
        return "{} ({})".format(self.name, self.code)
