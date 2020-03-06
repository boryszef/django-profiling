import csv
import os
from itertools import islice
from urllib.parse import urlparse
from urllib.request import urlretrieve

from django.conf import settings
from django.core.management import BaseCommand

from api.models import Country, Continent


class Command(BaseCommand):

    _sources = {
        Continent: "https://raw.githubusercontent.com/datasets/continent-codes/master/data/continent-codes.csv",
        Country: "https://raw.githubusercontent.com/datasets/country-codes/master/data/country-codes.csv"
    }
    # "https://raw.githubusercontent.com/datasets/airport-codes/master/data/airport-codes.csv"
    _batch_size = 500

    def handle(self, *args, **options):
        dir_name = self._make_data_directory()
        foreign_keys = {}

        continent_file_path = self._get_data_file(self._sources[Continent], dir_name)
        continents = self._populate_model(Continent, continent_file_path)
        foreign_keys[Continent._meta.model] = set(c.pk for c in continents)

        country_file_path = self._get_data_file(self._sources[Country], dir_name)
        countries = self._populate_model(Country, country_file_path, foreign_keys=foreign_keys)

    @staticmethod
    def _make_data_directory():
        dir_name = settings.DATA_DIR
        if not os.access(dir_name, os.F_OK):
            os.mkdir(dir_name)
        return dir_name

    def _get_data_file(self, data_file, dir_name):
        url = urlparse(data_file)
        target_name = os.path.split(url.path)[-1]
        target_path = os.path.join(dir_name, target_name)
        if not os.access(target_path, os.F_OK):
            self.stdout.write('Retrieving {} to {}'.format(data_file, target_path))
            urlretrieve(data_file, target_path)
        return target_path

    def _populate_model(self, model, target_path, foreign_keys=None):
        model.objects.all().delete()
        created = []
        generator = self._model_instance_generator(model, target_path, foreign_keys)
        while True:
            batch = list(islice(generator, self._batch_size))
            if not batch:
                break
            created.extend(model.objects.bulk_create(batch, self._batch_size))
            self.stdout.write('Created {} entries of {}'.format(len(created), model))
        return created

    @staticmethod
    def _model_instance_generator(model, target_path, foreign_keys=None):
            row_to_model = verbose_name_model_converter(model, foreign_keys)
            with open(target_path, encoding='utf-8') as csv_file:
                for idx, row in enumerate(csv.DictReader(csv_file, delimiter=',')):
                    instance = row_to_model(row)
                    yield instance


def verbose_name_model_converter(model, foreign_keys=None):
    """
    Factory to create a converter function that translates CSV entry into model instance.
    """
    if foreign_keys is None:
        foreign_keys = {}

    converter = {}
    many2one = {}
    for field in model._meta.get_fields():
        if not field.is_relation:
            converter[field.verbose_name] = field.name
        elif field.many_to_one:
            relation = foreign_keys[field.related_model]
            many2one[field.verbose_name] = (field.name + '_id', relation)

    def row_to_model(row):
        params = {}
        for key, val in row.items():
            if key in converter:
                _key = converter[key]
                params[_key] = val
            elif key in many2one and val in many2one[key][1]:
                _key = many2one[key][0]
                params[_key] = val

        return model(**params)

    return row_to_model
