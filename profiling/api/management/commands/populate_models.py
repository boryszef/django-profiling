import csv
import os
from datetime import datetime
from itertools import islice
from urllib.parse import urlparse
from urllib.request import urlretrieve

from django.conf import settings
from django.core.management import BaseCommand

from api.models import Country, Continent, Airport, City, Currency


class Command(BaseCommand):

    _sources = {
        Continent: "https://raw.githubusercontent.com/datasets/continent-codes/master/data/continent-codes.csv",
        Country: "https://raw.githubusercontent.com/datasets/country-codes/master/data/country-codes.csv",
        Airport: "https://raw.githubusercontent.com/datasets/airport-codes/master/data/airport-codes.csv",
        City: "https://raw.githubusercontent.com/datasets/world-cities/master/data/world-cities.csv",
        Currency: "https://raw.githubusercontent.com/datasets/currency-codes/master/data/codes-all.csv",
        # https://gist.githubusercontent.com/lunohodov/1995178/raw/cb8cf1ebe1d1b8fa5759e287ebd6eaecbe3bc3e4/ral_standard.csv
    }
    _batch_size = 1000

    def handle(self, *args, **options):
        dir_name = self._make_data_directory()
        foreign_keys = {}

        continent_file_path = self._get_data_file(self._sources[Continent], dir_name)
        continents = self._populate_model(Continent, ContinentConverter, continent_file_path)
        foreign_keys[Continent] = continents

        country_file_path = self._get_data_file(self._sources[Country], dir_name)
        countries = self._populate_model(Country, CountryConverter, country_file_path, foreign_keys=foreign_keys)
        foreign_keys[Country] = countries

        airport_file_path = self._get_data_file(self._sources[Airport], dir_name)
        airports = self._populate_model(Airport, AirportConverter, airport_file_path, foreign_keys=foreign_keys)

        city_file_path = self._get_data_file(self._sources[City], dir_name)
        cities = self._populate_model(City, CityConverter, city_file_path, foreign_keys=foreign_keys)

        currency_file_path = self._get_data_file(self._sources[Currency], dir_name)
        currencies = self._populate_model(Currency, CurrencyConverter, currency_file_path, foreign_keys=foreign_keys)

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

    def _populate_model(self, model, model_converter_class, target_path, foreign_keys=None):
        model.objects.all().delete()
        created = []
        model_converter = model_converter_class(foreign_keys)
        generator = self._model_instance_generator(model_converter, target_path)
        while True:
            batch = list(islice(generator, self._batch_size))
            if not batch:
                break
            created.extend(model.objects.bulk_create(batch, self._batch_size))
            self.stdout.write('Created {} entries of {}'.format(len(created), model))
        return created

    @staticmethod
    def _model_instance_generator(model_converter, target_path):
            with open(target_path, encoding='utf-8') as csv_file:
                for idx, row in enumerate(csv.DictReader(csv_file, delimiter=',', quotechar='"')):
                    instance = model_converter.convert(row)
                    yield instance


class ModelConverterBase(object):
    model = None

    def __init__(self, foreign_keys=None):
        self.foreign_keys = self._get_fkeys_pks(foreign_keys) if foreign_keys else {}
        fields = self.model._meta.get_fields()
        self.verbose_names = {f.verbose_name: f.name for f in fields if hasattr(f, 'verbose_name')}
        self.relations = {f.name: f.related_model for f in fields if f.is_relation}

    def _get_fkeys_pks(self, fkeys):
        pks = {}
        for model, instances in fkeys.items():
            pks[model._meta.model] = set(i.pk for i in instances)
        return pks

    def _update_default(self, params, key, value):
        if key not in self.relations:
            params[key] = value
            return
        relation_name = self.relations[key]
        relation = self.foreign_keys[relation_name]
        _val = value if value in relation else None
        _key = '{}_id'.format(key)
        params[_key] = _val

    def convert(self, row):
        params = {}
        for key, val in row.items():
            if key not in self.verbose_names:
                continue
            _key = self.verbose_names[key]
            converter_name = 'update_{}'.format(_key)
            converter = getattr(self, converter_name, self._update_default)
            converter(params, _key, val)
        return self.model(**params)


class ContinentConverter(ModelConverterBase):
    model = Continent


class CountryConverter(ModelConverterBase):
    model = Country

    def update_languages(self, params, key, value):
        params[key] = value.split(',')


class AirportConverter(ModelConverterBase):
    model = Airport

    def update_elevation(self, params, key, value):
        try:
            _val = float(value) * 0.3048
        except ValueError:
            return
        params[key] = _val

    def update_latitude(self, params, key, value):
        _val = value.split(',')
        if len(_val) != 2:
            return
        lat = float(_val[0])
        lon = float(_val[1])
        params['latitude'] = lat
        params['longitude'] = lon

    def update_longitude(self, params, key, value):
        self.update_latitude(params, key, value)


class CityConverter(ModelConverterBase):
    model = City

    def __init__(self, foreign_keys=None):
        super(CityConverter, self).__init__(foreign_keys)
        self.country_names = {c.official_name: c.pk for c in foreign_keys[Country]}

    def update_country(self, params, key, value):
        pk = self.country_names.get(value.title(), None)
        if pk is None:
            return
        _key = key + '_id'
        params[_key] = pk


class CurrencyConverter(CityConverter):
    model = Currency

    def update_withdrawal_date(self, params, key, value):
        try:
            _val = datetime.strptime(value, '%Y-%m').date()
        except ValueError:
            return
        params[key] = _val
