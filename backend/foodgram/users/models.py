from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'

    USER_ROLE = (
        (USER, 'User role'),
        (ADMIN, 'Administrator role'),
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Уникальное имя',
        help_text='Введите уникальное имя пользователя'
    )
    password = models.CharField(
        max_length=150,
        verbose_name='пароль'
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя',
        help_text='Введите имя пользователя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия',
        help_text='Введите фамилию пользователя'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта',
        help_text='Введите электронную почту пользователя'
    )
    is_subscribed = models.BooleanField(
        default=False,
        verbose_name='Подписка на данного пользователя',
        help_text='Отметьте для подписки на данного пользователя'
    )
    role = models.CharField(
        'Пользовательская роль',
        max_length=15,
        choices=USER_ROLE,
        default=USER
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь',
        help_text='Выберите пользователя, который подписывается'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
        help_text='Выберите автора, на которого подписываются'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        # constraints = (
        #     models.UniqueConstraint(fields=('user', 'following'),
        #                             name='unique_subscribe'),
        # )

    def __str__(self):
        return f'{self.user} {self.following}'
