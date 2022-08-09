# Generated by Django 2.2.19 on 2022-08-09 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(help_text='Выберите автора рецепта', on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(help_text='Выберите ингредиенты', related_name='ingredients', through='recipes.IngredientMount', to='recipes.Ingredient', verbose_name='Ингредиент'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(help_text='Выберите тэги', related_name='tags', through='recipes.TagRecipe', to='recipes.Tag', verbose_name='Тэг'),
        ),
        migrations.AddField(
            model_name='ingredientmount',
            name='ingredient',
            field=models.ForeignKey(help_text='Добавьте продукты, необходимые по рецепту', on_delete=django.db.models.deletion.CASCADE, related_name='recipe_ingredients', to='recipes.Ingredient', verbose_name='Продукты рецепта'),
        ),
        migrations.AddField(
            model_name='ingredientmount',
            name='recipe',
            field=models.ForeignKey(help_text='Выберите рецепт', on_delete=django.db.models.deletion.CASCADE, related_name='recipe_ingredients', to='recipes.Recipe', verbose_name='Рецепт'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(help_text='Выберите рецепт', on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='recipes.Recipe', verbose_name='Рецепт'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(help_text='Выберите пользователя', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='cart',
            name='recipe',
            field=models.ForeignKey(help_text='Выберите рецепты для добавления в корзины', on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart', to='recipes.Recipe', verbose_name='Рецепт'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(help_text='Выберите пользователя', on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_user_favorite_recipe'),
        ),
        migrations.AddConstraint(
            model_name='cart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_user_cart_recipe'),
        ),
    ]
