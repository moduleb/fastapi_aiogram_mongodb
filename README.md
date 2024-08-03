![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-%0c584b?style=for-the-badge&logo=fastapi&logoColor=white)
![Aiogram](https://img.shields.io/badge/Aiogram-white?style=for-the-badge&logo=chatbot&color=%234796EC)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

**Компоненты:**
- Веб-приложение на FastAPI
- Веб-сервер Nginx
- База данных MongoDB
- Телеграм-бот на Aiogram 3

**Возможности:**
- Создание сообщения с помощью запроса к API или через бота
- Просмотр всех сообщений с помощью запроса к API или через бота
- Сохранение IP-адреса отправителя
- Сохранение username отправителя (при работе через бота — автоматически, при запросе к API — опционально, можно указать вручную)


## Запуск:
>Для запуска вам потребуется [установить Docker](https://www.docker.com/).  
1. Клонировать проект с Github:
```bash
  git clone https://github.com/moduleb/fastapi_aiogram_mongodb.git
```

2. Перейти в папку проекта:
```bash
  cd fastapi_aiogram_mongodb
```

3. Создать файл .env, вписать токен от телеграм бота в формате TOKEN=ваш_токен:
```bash
nano .env
```

4. Запустить приложение:
```bash
sudo docker compose up -d --build
```

5. Остановить приложение:
```bash
sudo docker compose stop
```
-----------------------------------------------------
## Эндпоинты:

Приложение доступно по адресу:
- на локальной машине http://0.0.0.0/:80
- на удаленном сервере http://<IP адрес сервера>:80

### 
### **[post]** .../api/v1/messages

Принимает JSON с данными нового пользователя:
```json
{
  "content": "string",
  "username": "string" #опционально
}
```

Возвращает данные созданного сообщения:
```json
{
    "content": "string", #текст сообщения
    "host": "172.18.0.5", #ip адрес отправителя (локальный адрес, если отправлено через бота)
    "username": "string" #гusername пользователя, если отправлено через бота (при запросе к апи, может быть указано опционально)
}
```
###
### **[get]** .../api/v1/messages

Возвращает все сохраненные сообщения:
```json
[
    {
        "content": "test",
        "host": "192.168.65.1",
        "username": "user"
    },
    {
        "content": "dfgtjh",
        "host": "172.18.0.4",
        "username": "popcorn138"
    },
]
