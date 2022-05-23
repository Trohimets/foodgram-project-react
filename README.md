# Cервис для публикаций и обмена рецептами.

Авторизованные пользователи могут подписываться на понравившихся авторов, добавлять рецепты в избранное, в покупки, скачивать список покупок. Неавторизованным пользователям доступна регистрация, авторизация, просмотр рецептов других пользователей.

## Стек технологий
Python 3.9.7, Django 3.2.7, Django REST Framework 3.12, PostgresQL, Docker, Yandex.Cloud.

## Описание проекта и функционала

### Главная страница

Содержимое главной страницы — список рецептов, отсортированных по дате публикации (от новых к старым).

### Страница рецепта

На странице — полное описание рецепта, возможность добавить рецепт в избранное и в список покупок, возможность подписаться на автора рецепта.

### Страница пользователя

На странице — имя пользователя, все рецепты, опубликованные пользователем и возможность подписаться на пользователя.

### Подписка на авторов

Подписка на публикации доступна только авторизованному пользователю. Страница подписок доступна только владельцу.

### Сценарий поведения пользователя:

- Пользователь переходит на страницу другого пользователя или на страницу рецепта и подписывается на публикации автора кликом по кнопке `Подписаться на автора`.
- Пользователь переходит на страницу «Мои подписки» и просматривает список рецептов, опубликованных теми авторами, на которых он подписался. Сортировка записей — по дате публикации (от новых к старым).
- При необходимости пользователь может отказаться от подписки на автора: переходит на страницу автора или на страницу его рецепта и нажимает `Отписаться от автора`.

### Список избранного
Работа со списком избранного доступна **только авторизованному** пользователю. Список избранного может просматривать **только его владелец**.  

**Сценарий поведения пользователя:**

- Пользователь отмечает один или несколько рецептов кликом по кнопке `Добавить в избранное`.
- Пользователь переходит на страницу `«Список избранного»` и просматривает персональный список избранных рецептов.
- При необходимости пользователь может `Удалить` рецепт из избранного.

### Список покупок
Работа со списком покупок доступна **авторизованным и не авторизованным** пользователям. 
Список покупок может просматривать **только его владелец**.
**Сценарий поведения пользователя:**

- Пользователь отмечает один или несколько рецептов кликом по кнопке `Добавить в покупки`.
- Пользователь переходит на страницу `Список покупок`, там доступны все добавленные в список рецепты. Пользователь нажимает кнопку `Скачать` список и получает файл с суммированным перечнем и количеством необходимых ингредиентов для всех рецептов, сохранённых в `«Списке покупок»`.
- При необходимости пользователь может удалить рецепт из списка покупок.

Список покупок скачивается в формате PDF.
При скачивании списка покупок ингредиенты в результирующем суммируются 
`если в двух рецептах есть сахар (в одном рецепте 5 г, в другом — 10 г), то в списке будет один пункт: Сахар — 15 г.`

### Фильтрация по тегам
При нажатии на название тега выводится список рецептов, отмеченных этим тегом. Фильтрация может проводится по нескольким тегам в комбинации «или»: если выбраны несколько тегов — на странице будут показаны рецепты, которые отмечены хотя бы одним из этих тегов.
При фильтрации на странице пользователя фильтруются только рецепты выбранного пользователя. 
При фильтрации на странице избранного фильтруются только избранные рецепты. 


### Регистрация и авторизация
В проекте доступна система регистрации и авторизации пользователей. 
Обязательные поля для пользователя:

    Логин
    Пароль
    Email

### Что могут делать неавторизованные пользователи

- Создать аккаунт.
- Просматривать рецепты на главной.
- Просматривать отдельные страницы рецептов.
- Просматривать страницы пользователей.
- Фильтровать рецепты по тегам.
- Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл с количеством необходимых ингредиентов для рецептов из списка покупок.

### Что могут делать авторизованные пользователи

- Входить в систему под своим логином и паролем.
- Выходить из системы (разлогиниваться).
- Восстанавливать свой пароль.
- Менять свой пароль.
- Создавать/редактировать/удалять собственные рецепты
- Просматривать рецепты на главной.
- Просматривать страницы пользователей.
- Просматривать отдельные страницы рецептов.
- Фильтровать рецепты по тегам.
- Работать с персональным списком избранного: добавлять/удалять чужие рецепты, просматривать свою страницу избранных рецептов.
- Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл с количеством необходимых ингредиентов для рецептов из списка покупок.
- Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок.

# Подготовка к запуску и запуск проекта foodgram

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source venv/scripts/activate
```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Перейти в основную папку и выполнить миграции:

```
cd foodgram
```

Выполнить миграцию:

```
python manage.py migrate
```

Заполненить базу данных CSV-файлами:

```
python manage.py uploadDB tags.csv ingridients.csv
```

Запустить проект:

```
python manage.py runserver
```

