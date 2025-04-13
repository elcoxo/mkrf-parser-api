# mkrf-parser-api

Django REST API + Python парсер для реестра открытых данных Минкульта России.

##### Используемый в проекте реестр:

[Реестр прокатных удостоверений фильмов](https://opendata.mkrf.ru/opendata/7705851331-register_movies)

## Возможности:

* Асинхронная сборка данных с таблицы реестра Минкульта России в базу данных;
* REST API с доступом к данным;
* Возможность фильтрации и поиска по ключевым полям;
* Пагинация результатов с настраиваемым размером страницы;
* Автоматически генерируемая документация к API;
* Docker-образ, который парсит встроенную в него таблицу и поднимает сервер с базой данных и API;

## Используемый стек технологий:

* Python;
* Django REST Framework;
* SQLAlchemy;
* Asyncpg;
* Aiohttp;
* Pydantic;
* Pytest;
* Swagger;
* Docker + Docker Compose;

## Настройка конфигураций:

### Локальный запуск

1. Клонируем проект:

```
git clone https://github.com/elcoxo/mkrf-parser-api.git
```

2. Создайте файл .env на основе .env.example и заполните переменные окружения:

```
cp .env.example .env 
```

3. Первоначальная сборка проект с помощью Docker Compose:

```
docker-compose up --build
```

4. Далее образ можно запускать так:

```
docker-compose up
```

### Запуск через Docker Hub:

1. Скачайте образ из Docker Hub:

```
docker pull postgres:latest
docker pull temets/mkrf-parser:latest
docker pull temets/mkrf-django-api:latest
```

2. Для тома pg_data создадим Docker volume:

```
docker volume create pg_data
```

3. Запуск образов:

<details>

<summary>Содержимое команд для запуска образов</summary>

Запуск образа БД PostgreSQL:

```
docker run -d \
  --name db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=mkrf_db \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v pg_data:/var/lib/postgresql/data/pgdata \
  -p 5432:5432 \
  --network mkrf-network \
  --restart always \
  postgres:latest
```

Запуск образа Django REST API:

```
docker run -d \
  --name django \
  -e DB_NAME=mkrf_db \
  -e DB_USER=postgres \
  -e DB_PASS=postgres \
  -e DB_HOST=db \
  -e DB_PORT=5432 \
  -p 8000:8001 \
  --network mkrf-network \
  --restart on-failure \
  temets/mkrf-django-api:latest
```

Запуск образа парсера:

```
docker run -d \
  --name parser \
  -e DB_NAME=mkrf_db \
  -e DB_USER=postgres \
  -e DB_PASS=postgres \
  -e DB_HOST=db \
  -e DB_PORT=5432 \
  --network mkrf-network \
  --restart on-failure \
  temets/mkrf-parser:latest
```

</details>

## Дерево проекта:

### api/ — Django API приложение

- `config/` — настройки Django проекта;
- `register_movies/` — приложение для
  работы [с реестром фильмов;](https://opendata.mkrf.ru/opendata/7705851331-register_movies)
- `tests/` — тесты для API и приложения `register_movies`;
- `manage.py` — стандартный файл для управления Django проектом.

### parsers/ — Каталог для асинхронного парсера.

- `config/` — содержит базовые настройки и подключение к БД;
    - `config/base.py` — базовые классы с методами для работы с БД;
    - `config/database.py` — настройка и классы для подключения к БД;
- `register_movies/` — модуль для работы с реестром фильмов(DAO, модели, схемы, функции для парсинга);
- `entrypoint.sh` — точка входа для парсера;

## Модели:

Для работы парсинга и API были отобраны признаками,
которые отображаются непосредственно в таблице на странице реестра прокатных удостоверений фильмов.

![Frame 2](https://github.com/user-attachments/assets/2d77ed97-352d-4c63-850d-fd6b89885c73)

Практически весь реестр состоит из неструктурированных данных, кроме дат и идентификатор записи реестра.
Остальные признаки представлены в виде строк, часто содержащих артефакты.

![Frame 3](https://github.com/user-attachments/assets/dea18816-3648-4a96-94cc-f132af8537ff)

### Django модель

RegisterMovie

```python
class RegisterMovie(models.Model):
    registry_id: int = models.PositiveIntegerField(verbose_name='Идентификатор записи реестра')
    card_number: int = models.TextField(verbose_name='Номер удостоверения', null=True, blank=True)
    film_name: str = models.TextField(verbose_name='Название фильма')
    card_date: date = models.DateField(verbose_name='Дата регистрации удостоверения', null=True, blank=True)
    director: str = models.TextField(verbose_name='Режиссер', null=True, blank=True)
    studio: str = models.TextField(verbose_name='Студия-производитель', null=True, blank=True)
    category: str = models.CharField(max_length=100, verbose_name='Категория', null=True, blank=True)
    view_movie: str = models.CharField(max_length=100, verbose_name='Вид фильма', null=True, blank=True)
    color: str = models.CharField(max_length=100, verbose_name='Цвет', null=True, blank=True)
    age_category: str = models.TextField(verbose_name='Возрастная категория', null=True, blank=True)
    start_date_rent: date = models.DateField(verbose_name='Дата начала показа фильма', null=True, blank=True)
    year_of_production: int = models.TextField(verbose_name='Год производства', null=True, blank=True)
    country_of_production: str = models.TextField(verbose_name='Страна производства', null=True, blank=True)

    class Meta:
        db_table = "register_movies"
```

# API  Эндпроинты:

### [GET] Список всех записей RegisterMovie

#### Запрос

```
GET http://localhost:8000/api/v1/register_movies
```

Есть поддержка поиска, фильтрации и пагинации через инструменты DRF и библиотеки django-filter.

#### Фильтрация

Реализация через класс `RegisterMovieFilter` в `api/register_movies/filters.py`.

Доступные операции:

* `exact` – точное совпадение, учитывая регистр;
* `iexact` – точное совпадение, игнорируя регистр;
* `icontains` – частичное совпадение;
* `lt` – даты меньше указанного значения;
* `gt` – даты больше указанного значения;
* `range` – диапазон дат;

```
GET http://localhost:8000/api/v1/register_movies/?film_name__icontains=Титаник
```

```
GET http://localhost:8000/api/v1/register_movies/?ordering=id&start_date_rent__range=2021-01-01,2021-12-31
```

#### Поиск

Реализация через класс `SearchFilter` из DRF. Полнотекстовый поиск выполняется,
как на сайте Минкульта РФ, через все поля(кроме дат). Поиск выполняется с помощью параметра `search`

```
GET http://localhost:8000/api/v1/register_movies/?search=Похожи
```

#### Пагинация

Реализация через кастомный класс, наследуемый от `PageNumberPagination` из DRF.

Доступные операции:

* `page` – параметр для указания номера страницы;
* `size` – параметр для указания размера страницы(100 записей максимум);

```
GET http://localhost:8000/api/v1/register_movies/?page=2&size=15
```

#### Ответ

* `links` – Информация о навигации по страницам пагинации;
    * `current` – Текущая страница списка;
    * `next` – Ссылка на следующую страницу списка;
    * `previous` – Ссылка на предыдущую страницу списка;
    * `last` – Последняя страница списка;
* `count` – Общее количество записей в реестре;
* `countItemsOnPage` – Количество записей, отображаемых на текущей странице;

```
{
    "links": {
        "current": 1,
        "next": "http://localhost:8000/api/v1/register_movies?page=2",
        "previous": null,
        "last": 45703
    },
    "count": 457030,
    "countItemsOnPage": 10,
    "results": [
        {
            "id": 1,
            "registry_id": 6867567,
            "card_number": "213005721",
            "film_name": "Похожи ли мы?",
            "card_date": "2021-11-29",
            "director": "Е. Велихова",
            "studio": "Велихова Екатерина Дмитриевна",
            "category": "Видео",
            "view_movie": "Научно-популярный",
            "color": "Цветной+Черно-белый",
            "age_category": "«12+» для детей старше 12 лет",
            "start_date_rent": "2021-12-01",
            "year_of_production": "2021",
            "country_of_production": "Россия"
        },
        ...
    ]
}
```

### [POST] Создание новой записей RegisterMovie

```
POST http://localhost:8000/api/v1/register_movies
```

Пример Json файла:

```
{
    "registry_id": 6432101,
    "card_number": "112001621",
    "film_name": "Battle",
    "card_date": "2021-06-09",
    "director": "И.Белов",
    "studio": "ООО Арт Пикчерс Студия",
    "category": "Кино",
    "view_movie": "Документальный",
    "color": "Цветной",
    "age_category": "«12+» для детей старше 12 лет",
    "start_date_rent": "2021-06-30",
    "year_of_production": "2021",
    "country_of_production": "Россия"
}
```

### [GET] Вывод одной записи RegisterMovie по ID:

```
GET http://localhost:8000/api/v1/register_movies/{id}
```

### [PATCH] Редактирование полей одной записи RegisterMovie по ID:

```
PATCH http://localhost:8000/api/v1/register_movies/{id}
```

Пример Json файла:

```
{
    "film_name": "Цемнадцать мгновений весны",
    "color": "Черно-белый",
}
```

### [DELETE] Удалить запись RegisterMovie по ID:

```
DELETE http://localhost:8000/api/v1/register_movies/{id}
```

## Документация

Полная документация реализованная на Swagger: http://localhost:8000/api/v1/docs/

![Frame 4](https://github.com/user-attachments/assets/f3a922bd-64b5-42db-8ed0-0e5b680a41f7)

# Парсер

Реализует асинхронный сбор данных с
использованием [XHR-запросов](https://opendata.mkrf.ru/datatable/register_movies_6013e9b63f75a075a5cb7599/).

![image](https://github.com/user-attachments/assets/49ec6686-3bbd-4a07-8570-3cae835eb15a)

Запросы собираются постранично(`aiohttp`) и выполняются пачками(`asyncio.gather`).

![image](https://github.com/user-attachments/assets/82144238-2aaa-43e2-8f1e-2c69c34fd17b)

Параметры для оптимизации работы парсера:

* `PAGE_SIZE` – размер страницы;
* `REQUEST_RATE` – количество параллельных запросов;

# Тесты, линтеры и CI/CD

Структура проекта предполагает разделения тестов для каждого приложения. Для Django API приложения `register_movies`
разработан набор тестов с использованием `pytest` для проверки фильтрации, создания модели, сериализации и
работоспособности API.

В проекте также используется линтер `Ruff` и `Flake8` для проверки кода на соответствие стандартам PEP8

Для автоматизации тестирования и линтинга настроена CI/CD с использованием GitHub Actions. Конфигурация запускает 2
процесса:

* `lint` – проверка кода используя линтер `Ruff`
* `test` – запуск тестов `pytest`


![image](https://github.com/user-attachments/assets/abebb5c9-b413-4da3-b722-818dbf5f1f47)

