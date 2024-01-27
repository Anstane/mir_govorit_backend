from django.shortcuts import render
from django.db.models import Q

from .models import Recipe, Product, RecipeProduct


def add_product_to_recipe(request, recipe_id, product_id, weight):
    pass


def cook_recipe(request, recipe_id):
    pass


def show_recipes_without_product(request, product_id):
    """
    Функция генерирует таблицу, 
    в которой отображаются ID рецептов
    с отсутсвующими product_id (или их меньше 10 грамм).
    """

    recipes_without_product = Recipe.objects.exclude(
        recipeproduct__product_id=product_id
    )
    recipes_with_less_than_10g = Recipe.objects.filter(
        recipeproduct__product_id=product_id,
        recipeproduct__weight__lt=10
    )
    unique_recipes = recipes_without_product.union(
        recipes_with_less_than_10g
    )

    product = Product.objects.get(
        id=product_id
    )

    context = {
        'product': product,
        'recipes': unique_recipes
    }

    return render(request, 'recipe.html', context)
 