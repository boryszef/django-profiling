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

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.existing_objects = {}

    def handle(self, *args, **options):

        dir_name = self._make_data_directory()

        for model, data_file in self._data_files.items():
            self._get_existing_objects(model)
            target_path = self._get_data_file(data_file, dir_name)
            self._populate_model(model, target_path)

    def _populate_titles(self, dir_name):
        model = Title
        data_file = self._data_files[model]
        self._get_existing_objects(model)
        target_path = self._get_data_file(data_file, dir_name)
        created_titles = self._populate_model(model, target_path)
        return created_titles

    def _get_existing_objects(self, model):
        self.existing_objects[model] = set(model.objects.values_list('pk', flat=True))

    def _get_data_file(self, data_file, dir_name):
        url = urlparse(data_file)
        target_name = os.path.split(url.path)[-1]
        target_path = os.path.join(dir_name, target_name)
        if not os.access(target_path, os.F_OK):
            self.stdout.write('Retrieving {} to {}'.format(data_file, target_path))
            urlretrieve(data_file, target_path)
        return target_path

    def _make_data_directory(self):
        dir_name = settings.TSV_DATA_DIR
        if not os.access(dir_name, os.F_OK):
            os.mkdir(dir_name)
        return dir_name

    def _populate_model(self, model, target_path, max_entries=None):
        created = []
        generator = self._model_instance_generator(model, target_path)
        while True:
            batch = list(islice(generator, self._batch_size))
            if not batch or (max_entries and len(created) > max_entries):
                break
            created.extend(model.objects.bulk_create(batch, self._batch_size))
            self.stdout.write('Created {} entries of {}'.format(len(created), model))
        return created

    def _model_instance_generator(self, model, target_path):
        row_to_model = row_to_model_converter(model)
        with gzip.open(target_path, 'rt', encoding='utf-8') as tsv_file:
            for row in csv.DictReader(tsv_file, delimiter='\t'):
                instance = row_to_model(row)
                if instance.pk in self.existing_objects[model]:
                    continue
                yield instance


def row_to_model_converter(model):
    model_name = model._meta.model_name
    converter_mapping = {
        'title': {
            'tconst': lambda row: row['tconst'],
            'primary_title': lambda row: row['primaryTitle'],
            'original_title': lambda row: row['originalTitle'],
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
