# Ubiquiti Assignment

## Environment Setup

```sh
pyenv virtualenv ubiquiti
pyenv activate ubiquiti
pip install -r requirements.txt
```

## Launch Dependencies

```sh
docker-compose up
```

## Launch App

```sh
python ui.py db reset
django-admin runserver --pythonpath=. --settings=app
```
