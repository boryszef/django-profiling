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
