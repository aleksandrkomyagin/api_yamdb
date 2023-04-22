# YaMDb REST API
##### Проект YaMDb собирает отзывы пользователей на различные произведения. 
&nbsp;
## Функционал:
+ Регистрация пользователей
+ Получение JWT-токена по коду подтверждения
+ Аутентификация по JWT-токену и username
+ Работа со списком произведений, категориями, жанрами, отзывами, комментариями: создание, получение, редактирование, удаление, обновление
+ Получение информации о пользователе по username(Администратор)
+ Просмотр информации собственного профиля


## Используемые технологии:
| Название | Документация |
| ------ | ------ |
| Python 3.9.10 | [https://www.python.org/downloads/release/python-3910/][python] |
| Django | [https://www.djangoproject.com/][django] |
| django-rest-framework | [https://www.django-rest-framework.org/][DRF] |
| django-rest-framework-simplejwt | [https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html][simplejwt] |
| Djoser | [https://djoser.readthedocs.io/en/latest/][djoser] |
| Django-filter | [https://django-filter.readthedocs.io/en/main/][django-filter] |

## Установка
#### 1. Клонировать репозиторий
```
$ git@github.com:aleksandrkomyagin/api_yamdb.git
```
#### 2. Cоздать и активировать виртуальное окружение:
```
$ cd api_yamdb 
$ python3 -m venv venv
```
Активация виртуального окружения на *unix-подобных системах
```
$ source venv/bin/activate
```
Активация виртуального окружения на Windows
```
$ source venv/Scripts/activate
```
#### 3. Установить зависимости из файла requirements.txt:
```
(venv) $ python3 -m pip install --upgrade pip
(venv) $ pip install -r requirements.txt
```
#### 4. Выполнить миграции:
```
(venv) $ python3 manage.py migrate
```
#### 5. Импортировать данные из csv-файлов в базу:
```
(venv) $ python3 manage.py load_data
```
#### 6. Запустить сервер
```
(venv) $ python3 manage.py runserver
```
>  После установки проект доступен по адресу 127.0.0.1:8000/

&nbsp;
&nbsp;
&nbsp;
## Примеры API запросов и ответов 
##### 1. POST-запрос неавторизованного пользователя к эндпоинту [http://127.0.0.1:8000/api/v1/auth/signup/](http://127.0.0.1:8000/api/v1/auth/signup/). 
&nbsp;
Тело запроса:
```
{
    "username": "Tester",
    "email": "test@mail.ru"
}
```

Ответ API:
```
{
    "username": "Tester",
    "email": "test@mail.ru"
}
```
##### 2. POST-запрос неавторизованного пользователя, с адресом эл.почты, который уже есть в базе, к эндпоинту [http://127.0.0.1:8000/api/v1/auth/signup/](http://127.0.0.1:8000/api/v1/auth/signup/). 
&nbsp;
Тело запроса:
```
{
    "username": "Tester2",
    "email": "test@mail.ru"
}
```

Ответ API:
```
{
    "Ошибка": "UNIQUE constraint failed: users_user.email"
}
```
##### 3. POST-запрос неавторизованного пользователя к эндпоинту [http://127.0.0.1:8000/api/v1/auth/token/](http://127.0.0.1:8000/api/v1/auth/token/). 
&nbsp;
Тело запроса:
```
{
    "username": "Tester",
    "confirmation_code": "66c38d5d-2f8c-402e-b826-9fe83ce39bc4"
}
```
Ответ API:
```
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgxODQxMTc1LCJpYXQiOjE2ODE3NTQ3NzUsImp0aSI6IjVmNDQ2OWVjZjg0MzRhYzk4YzllMzIwMWJmMDc0YjczIiwidXNlcl9pZCI6MTA2fQ.mqNe82qU8m--FMtrNggcKAgyWEHwxc8tPqD14xTiGks"
}
```
##### 4. GET-запрос пользователя без токена к эндпоинту [http://127.0.0.1:8000/api/v1/categories/](http://127.0.0.1:8000/api/v1/categories/). 
&nbsp;
Ответ API:
```
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "name": "Книга",
            "slug": "book"
        },
        {
            "name": "Фильм",
            "slug": "movie"
        },
        {
            "name": "Музыка",
            "slug": "music"
        }
    ]
}
```
##### 5. GET-запрос пользователя без токена к эндпоинту [http://127.0.0.1:8000/api/v1/genres/](http://127.0.0.1:8000/api/v1/genres/). 
&nbsp;
Ответ API:
```
{
    "count": 15,
    "next": "http://127.0.0.1:8000/api/v1/genres/?limit=10&offset=10",
    "previous": null,
    "results": [
        {
            "name": "Баллада",
            "slug": "ballad"
        },
        {
            "name": "Шансон",
            "slug": "chanson"
        },
        {
            "name": "Классика",
            "slug": "classical"
        },
        {
            "name": "Комедия",
            "slug": "comedy"
        },
        {
            "name": "Детектив",
            "slug": "detective"
        },
        {
            "name": "Драма",
            "slug": "drama"
        },
        {
            "name": "Фэнтези",
            "slug": "fantasy"
        },
        {
            "name": "Гонзо",
            "slug": "gonzo"
        },
        {
            "name": "Рок",
            "slug": "rock"
        },
        {
            "name": "Rock-n-roll",
            "slug": "rock-n-roll"
        }
    ]
}
```
##### 6. GET-запрос авторизованного пользователя к эндпоинту [http://127.0.0.1:8000/api/v1/users/me/](http://127.0.0.1:8000/api/v1/users/me/). 
&nbsp;
Ответ API:
```
{
    "username": "Tester",
    "email": "test@mail.ru",
    "first_name": "",
    "last_name": "",
    "bio": "",
    "role": "user"
}
```
> Подробная информация о всех эндпоинтах по адресу http://127.0.0.1:8000/redoc/
&nbsp;
# Авторы проекта:
### Комягин Александр
[![Gmail Badge](https://img.shields.io/badge/-aleksandrkomyagin8@gmail.com-c14438?style=flat&logo=Gmail&logoColor=white&link=mailto:aleksandrkomyagin8@gmail.com)](mailto:aleksandrkomyagin8@gmail.com) 
### Шмыков Андрей
[![Gmail Badge](https://img.shields.io/badge/-andrey.shmykov88@gmail.com-c14438?style=flat&logo=Gmail&logoColor=white&link=mailto:andrey.shmykov88@gmail.com)](mailto:andrey.shmykov88@gmail.com)
### Розкалий Юрий
[![Gmail Badge](https://img.shields.io/badge/-uyriigerc@gmail.com-c14438?style=flat&logo=Gmail&logoColor=white&link=mailto:uyriigerc@gmail.com)](mailto:uyriigerc@gmail.com)

[//]:#

   [python]: <https://www.python.org/downloads/release/python-3910/>
   [simplejwt]: <https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html>
   [djoser]: <https://djoser.readthedocs.io/en/latest/>
   [django]: <https://www.djangoproject.com/>
   [DRF]: <https://www.django-rest-framework.org/>
   [django-filter]: <https://django-filter.readthedocs.io/en/main/>
