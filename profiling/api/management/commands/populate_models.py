import csv
import gzip
import os
from itertools import islice
from urllib.parse import urlparse
from urllib.request import urlretrieve

from django.conf import settings
from django.core.management import BaseCommand

from api.models import Title, Person


class Command(BaseCommand):

    _data_files = {
        Title: 'https://datasets.imdbws.com/title.basics.tsv.gz',
        Person: 'https://datasets.imdbws.com/name.basics.tsv.gz',
        #'https://datasets.imdbws.com/title.principals.tsv.gz'
    }
    _batch_size = 500

    def handle(self, *args, **options):

        dir_name = settings.TSV_DATA_DIR
        if not os.access(dir_name, os.F_OK):
            os.mkdir(dir_name)

        for model, data_file in self._data_files.items():
            url = urlparse(data_file)
            target_name = os.path.split(url.path)[-1]
            target_path = os.path.join(dir_name, target_name)
            if not os.access(target_path, os.F_OK):
                self.stdout.write('Retrieving {} to {}'.format(data_file, target_path))
                urlretrieve(data_file, target_path)
            self._populate_model(Title, target_path)

    def _populate_model(self, model, target_path):
        model.objects.all().delete()
        created_count = 0
        generator = self._model_instance_generator(model, target_path)
        while True:
            batch = list(islice(generator, self._batch_size))
            if not batch:
                break
            created = model.objects.bulk_create(batch, self._batch_size)
            created_count += len(created)
            self.stdout.write('Created {} entries of {}'.format(created_count, model))
            if created_count > 100000:
                break

    def _model_instance_generator(self, model, target_path):
        row_to_model = row_to_model_converter(model)
        with gzip.open(target_path, 'rt', encoding='utf-8') as tsv_file:
            for row in csv.DictReader(tsv_file, delimiter='\t'):
                yield row_to_model(row)


def row_to_model_converter(model):
    model_name = model._meta.model_name
    converter_mapping = {
        'title': {
            'tconst': lambda row: row['tconst'],
            'primary_title': lambda row: row['primaryTitle'],
            'genres': lambda row: row.get('genres', '').split(',')
        },
        'person': {
            'nconst': lambda row: row['nconst'],
            'primary_name': lambda row: row['primaryName'],
            'birth_year': lambda row: row['birthYear']
        }
    }
    converter = converter_mapping[model_name]

    def row_to_model(row):
        return model(**{key: converter[key](row) for key, val in row.items() if key in converter})

    return row_to_model
