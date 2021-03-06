# Generated by Django 2.2.10 on 2020-03-08 21:20

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Continent',
            fields=[
                ('code', models.CharField(max_length=2, primary_key=True, serialize=False, verbose_name='Code')),
                ('name', models.TextField(verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('alpha2', models.CharField(help_text='Alpha-2 codes from ISO 3166-1', max_length=2, primary_key=True, serialize=False, unique=True, verbose_name='ISO3166-1-Alpha-2')),
                ('alpha3', models.CharField(help_text='Alpha-3 codes from ISO 3166-1 (synonymous with World Bank Codes)', max_length=3, unique=True, verbose_name='ISO3166-1-Alpha-3')),
                ('dial', models.TextField(help_text='Country code from ITU-T recommendation E.164, sometimes followed by area code', verbose_name='Dial')),
                ('continent', models.ForeignKey(help_text='Continent from Geonames', null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Continent', verbose_name='Continent')),
                ('capital', models.TextField(help_text='Capital city from Geonames', verbose_name='Capital')),
                ('ds', models.CharField(help_text='Distinguishing signs of vehicles in international traffic', max_length=3, verbose_name='DS')),
                ('languages', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=list, help_text='Languages from Geonames', size=None, verbose_name='Languages')),
                ('formal_name', models.TextField(help_text="Country's formal English name from UN Protocol and Liaison Service", verbose_name='UNTERM English Formal')),
                ('official_name', models.TextField(help_text='Country or Area official English short name from UN Statistics Divsion', verbose_name='official_name_en')),
                ('short_name', models.TextField(help_text="Country's short English name from UN Protocol and Liaison Service", verbose_name='UNTERM English Short')),
            ],
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('ident', models.CharField(max_length=8, primary_key=True, serialize=False, verbose_name='ident')),
                ('type', models.TextField(verbose_name='type')),
                ('name', models.TextField(verbose_name='name')),
                ('elevation', models.FloatField(null=True, verbose_name='elevation_ft')),
                ('gps_code', models.CharField(max_length=4, verbose_name='gps_code')),
                ('iata_code', models.CharField(max_length=3, verbose_name='iata_code')),
                ('latitude', models.FloatField(verbose_name='coordinates')),
                ('longitude', models.FloatField(verbose_name='coordinates')),
                ('continent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Continent', verbose_name='continent')),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Country', verbose_name='iso_country')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='name')),
                ('subcountry', models.TextField(verbose_name='subcountry')),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Country', verbose_name='country')),
            ],
        ),
    ]
