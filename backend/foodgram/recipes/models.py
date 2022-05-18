from django.db import models
from django.contrib.auth.models import AbstractUser


USER = "user"
ADMIN = "admin"
ROLES = [
    ("user", USER),
    ("admin", ADMIN)
]


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        blank=True
    )
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    role = models.CharField(
        max_length=max(len(role) for _, role in ROLES),
        choices=ROLES,
        default=USER
    )


class Tag(models.Model):
    title = models.CharField(
        verbose_name='Тэг',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        max_length=50,
        unique=True
    )
    color = models.CharField('Цвет тэга', max_length=7)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Ingridient(models.Model):
    title = models.CharField(
        verbose_name='Ингридиент',
        max_length=256
    )
    amount = models.IntegerField(
        verbose_name='Количество'
    )
    unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=50
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


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
    description = models.TextField(verbose_name='Описание')
    ingridients = models.ManyToManyField(
        Ingridient,
        related_name='ingridients',
        verbose_name='Ингридиент',
        help_text='Выберите ингридиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        related_name='tags',
        verbose_name='Тэг',
        help_text='Выберите тэги'
    )
    time = models.IntegerField(
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
