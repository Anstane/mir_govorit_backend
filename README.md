# mir_govorit_backend


### Функционал:

- В приложении присутствуют 3 view функции (add_product_to_recipe, cook_recipe, show_recipes_without_product);
- Созданы 3 модели: 2 основных (Product, Recipe) и одна смежная для записи граммовки (RecipeProduct);
- Также сделана админка;
- Примеры запросов и логика расписаны в docstring`ах view функций.


### Стек:

Python 3.11 | Django 5.0.1 | SQLite


## Установка

#### Клонируем репозиторй
```
  git clone git@github.com:Anstane/mir_govorit_backend.git
```

#### Переходим в папку с приложением
```
  cd mir_govorit_backend/
```

### Запуск с помощью Docker:

#### Запускаем docker compose
```
  docker compose up
```

У нас также сразу создаются тестовые модели и админка (admin:admin).

### Запуск без Docker`а:

#### Создаём вируальное окружение и устанавливаем зависимости
```
  poetry shell
  poetry install
```

#### Делаем миграции
```
  python manage.py makemigrations
  python manage.py migrate
  python manage.py migrate --run-syncdb
```

#### Создаём модели и запускаем приложение
```
  python manage.py create_objects
  python manage.py runserver
```

#### Переходим на локальный адрес и пользуемся приложением


## Эндпоинты

### Добавить Продукт в Рецепт

Добавить продукт в рецепт с указанным весом.

**URL:** `/add_product_to_recipe/`

**Метод:** `GET`

**Параметры:**
- `recipe_id` (int): ID рецепта.
- `product_id` (int): ID продукта.
- `weight` (int): Вес продукта в граммах.

**Пример:**
```
  /add_product_to_recipe/?recipe_id=1&product_id=1&weight=150
```

### Приготовить Рецепт

Увеличить количество приготовленных блюд для каждого продукта в указанном рецепте.

**URL:** `/cook_recipe/`

**Метод:** `GET`

**Параметры:**
- `recipe_id` (int): ID рецепта.

**Пример:**
```
  /cook_recipe/?recipe_id=1
```

### Показать Рецепты без Продукта

Получить рецепты, где указанный продукт отсутствует или присутствует в количестве менее 10 грамм.

**URL:** `/show_recipes_without_product/<product_id>/`

**Метод:** `GET`

**Параметры:**
- `recipe_id` (int): ID рецепта.

**Пример:**
```
  /show_recipes_without_product/1/
```


## Автор

[Михаил Московкин](https://github.com/Anstane)