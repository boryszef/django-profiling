from django.contrib.postgres.fields import ArrayField
from django.db import models


class Title(models.Model):
    tconst = models.TextField(primary_key=True)
    primary_title = models.TextField()
    original_title = models.TextField()
    genres = ArrayField(base_field=models.TextField())
    cast_and_crew = models.ManyToManyField('Person', through='Personnel')

    def __repr__(self):
        return 'Title(tconst={})'.format(self.tconst)


class Person(models.Model):
    nconst = models.TextField(primary_key=True)
    primary_name = models.TextField()
    birth_year = models.DateField(null=True)


class Personnel(models.Model):
    tconst = models.ForeignKey(Title, on_delete=models.CASCADE)
    ordering = models.IntegerField()
    nconst = models.ForeignKey(Person, on_delete=models.CASCADE)
    category = models.TextField()

    class Meta:
        unique_together = ('tconst', 'ordering')


class Continent(models.Model):
    code = models.CharField(max_length=2, primary_key=True, verbose_name='Code')
    name = models.TextField(null=False, verbose_name='Name')


class Country(models.Model):
    alpha2 = models.CharField(max_length=2, unique=True, primary_key=True, verbose_name='ISO3166-1-Alpha-2')
    alpha3 = models.CharField(max_length=3, unique=True, verbose_name='ISO3166-1-Alpha-3')
    dial = models.TextField(verbose_name='Dial')
    name = models.TextField(verbose_name='Global Name')
    capital = models.TextField(verbose_name='Capital')
    continent = models.ForeignKey(Continent, null=True, on_delete=models.CASCADE, verbose_name='Continent')


#class Currency(models.Model):
    pass


#class Airport(models.Model):
#    ident = models.CharField(max_length=8, primary_key=True)
#    type = models.TextField()
#    name = models.TextField()
#    elevation = models.IntegerField()
#    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
#    iso_country
#    iso_region
#    municipality
#    gps_code
#    iata_code
#    local_code
#    latitude
#    longitude
