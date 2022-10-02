# bot_friend
Асинхронный бот предназначенный вести запись клиентов в парикмахерскую.

<br/>
Что умеет бот: <br/>
Владелец: <br/>

- Владелец может добавить администраторов (id телеграма владельца добавляется в переменные окружения OWNER=)

Администраторы:
- Администраторы могут добавить мастеров выбрав соответствующий пункт (даные сохраняются в БД)
  * Администраторы могут открыть рабочий день для мастера (рабочие часы будут сохранены в БД)
  * Администраторы могу удалить мастера из БД при увольнении 


>Переменные окружения прописываются в файле .env

<br/>Установка зависимостей: 

```
pip install -r requirements/requirements.txt
```

<br/>Применить миграции: 

```
make migrate
```
