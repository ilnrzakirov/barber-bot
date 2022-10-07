# bot_friend
Асинхронный бот предназначенный вести запись клиентов в парикмахерскую.

<br/>
Что умеет бот: <br/>

- Владелец:
  * Владелец может добавить администраторов (id телеграма владельца добавляется в переменные окружения OWNER=)
  * Владелец может удалить администратора из списка

- Администраторы:
  * Администраторы могут добавить мастера выбрав соответствующий пункт 
  * Администраторы могут открыть рабочий день для мастера 
  * Администраторы могут удалить мастера из БД при увольнении 
  * Администраторы могут смотреть отзывы
 
 - Клиент:
   * Выбрать мастера, записаться в удобное время
   * Посмотреть местоположение
   * Оставить отзыв


>Переменные окружения прописываются в файле .env

<br/>Установка зависимостей: 

```
pip install -r requirements/requirements.txt
```

<br/>Применить миграции: 

```
make migrate
```
