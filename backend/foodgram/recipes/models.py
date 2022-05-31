from django.db import models
from users.models import User

class Tag(models.Model):
    name = models.CharField(
        verbose_name='Тег',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        max_length=50,
        unique=True
    )
    color = models.CharField('Цвет тега', max_length=7)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Ингредиент',
        max_length=256
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=50
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        help_text='Автор рецепта'
    )
    name = models.CharField(
        verbose_name='Рецепт',
        help_text='Название рецепта',
        max_length=256
    )
    picture = models.ImageField(
        'Картинка',
        upload_to='recipes/',
        blank=True
    )  
    text = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientMount',
        related_name='ingredients',
        verbose_name='Ингредиент',
        help_text='Выберите ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        related_name='tags',
        verbose_name='Тэг',
        help_text='Выберите тэги'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class IngredientMount(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    mount = models.IntegerField(
        verbose_name='Количество ингредиента'
    )

    def __str__(self):
        return f'{self.ingredient} {self.recipe} {self.mount}'