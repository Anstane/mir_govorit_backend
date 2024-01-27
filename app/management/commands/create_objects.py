from django.core.management.base import BaseCommand
from app.models import Product, Recipe, RecipeProduct


class Command(BaseCommand):
    help = 'Создаём объекты для всех моделей.'

    def handle(self, *args, **kwargs):  
        product1 = Product.objects.create(name='Соль')
        product2 = Product.objects.create(name='Сахар')
        product3 = Product.objects.create(name='Мука')
        product4 = Product.objects.create(name='Яйцо')
        product5 = Product.objects.create(name='Шоколад')

        recipe1 = Recipe.objects.create(name='Яичница')
        recipe2 = Recipe.objects.create(name='Шоколадный торт')

        RecipeProduct.objects.create(recipe=recipe1, product=product1, weight_in_grams=9)
        RecipeProduct.objects.create(recipe=recipe1, product=product4, weight_in_grams=100)

        RecipeProduct.objects.create(recipe=recipe2, product=product2, weight_in_grams=50)
        RecipeProduct.objects.create(recipe=recipe2, product=product4, weight_in_grams=99)
        RecipeProduct.objects.create(recipe=recipe2, product=product5, weight_in_grams=250)

        self.stdout.write(self.style.SUCCESS('Объекты были созданы успешно.'))
