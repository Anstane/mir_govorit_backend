from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.db.models import F
from django.db import transaction, connection

from .models import Recipe, Product, RecipeProduct


def add_product_to_recipe(request):
    """
    Функция добавляет к указанному рецепту указанный продукт с указанным весом.

    Пример GET-запроса к функции: /add_product_to_recipe/?recipe_id=1&product_id=1&weight=150

    Логика функции:
    1) Получаем из GET-запроса необходимые параметры (recipe_id, product_id, weight).
    2) Запрашиваем объекты согласно id полученными из запроса.
    3) С помощью функции filter() проверяем есть ли такая связь в БД.
    4) Если связь есть -> перезаписываем вес в граммах.
    5) Если связи нет -> создаём её.
    """
    try:
        recipe_id = request.GET.get('recipe_id')
        product_id = request.GET.get('product_id')
        weight = request.GET.get('weight')

        if not recipe_id or not product_id or not weight:
            raise ValueError('Отсутствуют необходимые параметры.')

        with transaction.atomic(): # Обеспечиваем атомарность операции.
            recipe = get_object_or_404(Recipe, pk=recipe_id)
            product = get_object_or_404(Product, pk=product_id)

            recipe_product = RecipeProduct.objects.filter(recipe=recipe, product=product).first()

            if recipe_product:
                recipe_product.weight_in_grams = weight
                recipe_product.save()
            else:
                RecipeProduct.objects.create(recipe=recipe, product=product, weight_in_grams=weight)

            return HttpResponse('Данные по продукту и рецепту были обновлены.')

    except Recipe.DoesNotExist:
        return HttpResponseNotFound('Такого рецепта не существует.')

    except Product.DoesNotExist:
        return HttpResponseNotFound('Такого продукта нет.')
    
    except Exception as e:
        return JsonResponse({'message': str(e)})


def cook_recipe(request):
    """
    Функция прибавляет единицу к продуктам входящим в состав блюд.
    
    Пример GET-запроса к функции: /cook_recipe/?recipe_id=1

    Логика функции:
    1) Получаем  GET-запрос с параметором recipe_id.
    2) Получаем список рецептов по id.
    3) В цикле обращаемся ко всем продуктам из связанной модели RecipeProduct.
    4) Увеличиваем количество использованных раз на 1.
    5) Сохраняем изменённые данные.
    """

    try:
        recipe_id = request.GET.get('recipe_id')

        if not recipe_id:
            raise ValueError('Отсутствует необходимый параметр.')
        
        with transaction.atomic(): # Обеспечиваем атомарность операции.
            recipe = get_object_or_404(Recipe, pk=recipe_id)

            product_ids = recipe.recipeproduct_set.values_list('product_id')
            Product.objects.filter(id__in=product_ids).update(times_used=F('times_used') + 1)
            # Получаем id продуктов, которые будем изменять.
            # С помощью функции update() обновляем количество использований за 1 запрос к БД.
            # Функция F() в этом случае нужна для изменения значения прямо в БД и поддержания атомарности.

        return HttpResponse('Рецепт был приготовлен.')

    except Recipe.DoesNotExist:
        return HttpResponseNotFound('Такого рецепта не существует.')

    except Exception as e:
        return JsonResponse({'message': str(e)})


def show_recipes_without_product(request, product_id):
    """
    Функция генерирует таблицу с ID и названием рецептов,
    в которых либо отсуствует product_id, либо его содердание менее 10 грамм.

    Пример GET-запроса: /show_recipes_without_product/1/ (Где 1 - product_id)

    Логика функции:
    1) Получаем GET-запрос с указанием ID продукта.
    2) Составляем список рецептов без product_id.
    3) Составляем второй список, где product_id < 10 грамм.
    4) Функцией union() объединяем эти два списка.
    5) Получаем название продукта для Djnago шаблона.
    6) Рендерим Django шаблон с соотвествующим context`ом.
    """

    try:
        recipes_without_product = Recipe.objects.exclude(
            recipeproduct__product_id=product_id
        ) # Рецепты в которых отсутствует product_id.
        recipes_with_less_than_10g = Recipe.objects.filter(
            recipeproduct__product_id=product_id,
            recipeproduct__weight__lt=10
        ) # Проверяем, что количество этого продукта меньше 10.
        unique_recipes = recipes_without_product.union(
            recipes_with_less_than_10g
        ) # Объединение списка двух запросов.

        product = Product.objects.get(
            id=product_id
        ) # Получаем продукт для вывода названия в шаблоне.

        context = {
            'product': product,
            'recipes': unique_recipes
        }

        return render(request, 'recipe.html', context)

    except Product.DoesNotExist:
        return HttpResponseNotFound('Такого продукта нет.')
