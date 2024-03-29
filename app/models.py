from django.db import models


class Product(models.Model):
    """Модель продукта."""

    name = models.CharField(max_length=150)
    times_used = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Recipe(models.Model):
    """Модель рецепта, в которой может быть несколько продуктов."""

    name = models.CharField(max_length=150)
    product = models.ManyToManyField(Product, through='RecipeProduct')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeProduct(models.Model):
    """Модель для связи количества продукта в рецепте."""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight_in_grams = models.IntegerField()

    def __str__(self):
        return f'{self.product.name} - {self.weight_in_grams}г'

    class Meta: # Только уникальные продукты в рецепте.
        verbose_name = 'Рецепт - продукт'
        verbose_name_plural = 'Рецепты - продукты'
        constraints = (
            models.UniqueConstraint(
                fields=['recipe', 'product'],
                name='unique_recipe_product'
            ),
        )
