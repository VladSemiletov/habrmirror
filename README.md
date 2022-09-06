HabrMirror
===========


## Документация к проекту


Основные системные требования:
* Ubuntu 20.04 LTS
* Python 3.8+
* SQLLite 
* Django 



### Обновляем системные зависимости


```
~$ sudo apt update
~$ sudo apt upgrade
```


### Ставим SQLLite, создаём пользователя и БД


Для начала установим SQLLite, если он еще не установлен и проверим установленную версию. 

```
~$ sudo apt install sqlite3
~$ sqlite3 --version
```
и выполним следующие команды для создания базы данных 

```
sqlite3 habrmirror.db
```
Для запуска проекта локально выполним следующие команды:
```
~$ python3 manage.py makemigrations
~$ python3 manage.py migrate --run-syncdb 
~$ python manage.py createsuperuser
~$ python3 manage.py loaddata fixtures/fixtures.json
~$ python3 manage.py runserver
```
В фикстурах добавляется 4 категории и 12 статей.
```




