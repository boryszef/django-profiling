import csv
import gzip
import os
from itertools import islice
from urllib.parse import urlparse
from urllib.request import urlretrieve

from django.conf import settings
from django.core.management import BaseCommand

from api.models import Title, Person, Personnel


class Command(BaseCommand):

    _data_files = {
        Title: 'https://datasets.imdbws.com/title.basics.tsv.gz',
        Person: 'https://datasets.imdbws.com/name.basics.tsv.gz',
        Personnel: 'https://datasets.imdbws.com/title.principals.tsv.gz'
    }
    _batch_size = 500
    _sample_size = 100

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.existing_objects = {}

    def handle(self, *args, **options):

        dir_name = self._make_data_directory()
        title_ids = self._populate_titles(dir_name)
        principals = self._populate_principals(dir_name, title_ids)

    def _populate_titles(self, dir_name):
        model = Title
        model.objects.all().delete()
        data_file = self._data_files[model]
        target_path = self._get_data_file(data_file, dir_name)
        created_titles = self._populate_model(model, target_path, self._sample_size)
        return [obj.pk for obj in created_titles]

    def _populate_principals(self, dir_name, title_ids):
        model = Personnel
        data_file = self._data_files[model]
        target_path = self._get_data_file(data_file, dir_name)

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
        generator = self._model_instance_generator(model, target_path, max_entries)
        while True:
            batch = list(islice(generator, self._batch_size))
            if not batch:
                break
            created.extend(model.objects.bulk_create(batch, self._batch_size))
            self.stdout.write('Created {} entries of {}'.format(len(created), model))
        return created

    @staticmethod
    def _model_instance_generator(model, target_path, sample_size):
        """
        Generator method that yields approximately [sample_size] equally spaces entries from the file;
        entries are converted into instances of [model].
        """
        row_to_model = row_to_model_converter(model)
        line_count = get_approximate_line_count(target_path)
        every = line_count // sample_size
        with gzip.open(target_path, 'rt', encoding='utf-8') as tsv_file:
            for idx, row in enumerate(csv.DictReader(tsv_file, delimiter='\t')):
                instance = row_to_model(row)
                if idx % every:
                    continue
                yield instance


def get_approximate_line_count(file_name):
    """
    Calculate the approximate number of lines based on the length of the few initial lines and total file size.
    """
    sample = 2000
    file_size = os.stat(file_name).st_size
    avg_len = 0.0
    count = 0
    with gzip.open(file_name, 'rt', encoding='utf-8') as file:
        line = file.readline()
        while line and count < sample:
            avg_len += len(file.readline())
            count += 1
            line = file.readline()
    return int(file_size / avg_len * count)


def row_to_model_converter(model):
    """
    Factory to create a converter function that translates TSV entry into model instance.
    """
    model_name = model._meta.model_name
    converter_mapping = {
        'title': {
            'tconst': lambda row: row['tconst'],
            'primary_title': lambda row: row['primaryTitle'],
            'original_title': lambda row: row['originalTitle'],
            'genres': lambda row: (row.get('genres', '') or '').split(',')
        },
        'person': {
            'nconst': lambda row: row['nconst'],
            'primary_name': lambda row: row['primaryName'],
            'birth_year': lambda row: row['birthYear']
        }
    }
    converter = converter_mapping[model_name]

    def row_to_model(row):
        try:
            foo = model(**{key: converter[key](row) for key, val in row.items() if key in converter})
        except AttributeError:
            print(row)
            raise
        return foo

    return row_to_model
