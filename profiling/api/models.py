from django.contrib.postgres.fields import ArrayField
from django.db import models


class Title(models.Model):
    tconst = models.TextField(unique=True)
    primary_title = models.TextField()
    genres = ArrayField(base_field=models.TextField())

    def __repr__(self):
        return 'Title(tconst={})'.format(self.tconst)


class Person(models.Model):
    nconst = models.TextField(unique=True)
    primary_name = models.TextField()
    birth_year = models.DateField()


class Personnel(models.Model):
    tconst = models.ForeignKey(Title, on_delete=models.CASCADE)
    nconst = models.ForeignKey(Person, on_delete=models.CASCADE)
    category = models.TextField()
