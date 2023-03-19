# Canalservice

Сервис синхронизации базы данных с гугл-таблицами

## Стек

Django 4.0.6

PostgreSQL 14

Django_tables2

Gspread

## Инструкции по запуску проекта

git clone git@github.com:Konstantin8891/Canalservice.git

В папку infrastracture необходимо поместить файл с переменными окружения .env

Содержание файла .env

DB_ENGINE=django.db.backends.postgresql

DB_NAME=postgres

POSTGRES_USER=postgres

POSTGRES_PASSWORD=postgres

DB_HOST=db

DB_PORT=5432

SECRET_KEY=django-insecure-ze9gn5(5q&j!tzgm*_iuegpn7@bpcr_bf$5c8%gpxmghtkvaav

SPREADSHEET=1fArmA72nxcQVv_gr31MHv4RV2e_n8j79-xvr6FOWDDc

В папку с файлом manage.py необходимо поместить файл token.json с данными гугл авторизации

docker-compose up --build

docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py load_data

Этой командой запускается скрипт, которой должен всегда работать в фоне всегда. Он просыпается раз в 30 секунду и мониторит изменения.

Графическое представление доступно по адресу localhost

Таблица доступна по адресу

https://docs.google.com/spreadsheets/d/1fArmA72nxcQVv_gr31MHv4RV2e_n8j79-xvr6FOWDDc/edit#gid=0
