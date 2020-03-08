### Sample project utilizing Django & DRF

This is a sample project based on Django and Django REST Framework with few models related to each other and lots
of data in those models. Can be used as a boiler-plate for various backend-, django-, and DRF-related experiments.
In order to use it, simply do:
```shell script
git clone https://github.com/boryszef/django-profiling.git
cd ./django-profiling
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ./profiling
./manage.py migrate
./manage.py populate_models
./manage.py runserver
```
This will fetch data and fill models with instances, including Continent (7 instances), Countries (250 instances),
Cities (~23k instances) and Airports (~55k instances).