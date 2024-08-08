import logging
import os
import uvicorn
from bson import ObjectId
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from pymongo import MongoClient, errors

# Проверяем, запущено ли приложение в докере
is_running_in_docker = os.path.exists('/.dockerenv') or os.path.exists('/proc/1/cgroup')

# Создаем приложение FastAPI
app = FastAPI()

"""Устанавливаем строку подключения к MongoDB и
уровень логирования в зависимости от окружения"""
if is_running_in_docker:
    mongo_connection_string = "mongodb://mongo:27017/"
    log_level = logging.INFO
else:
    log_level = logging.DEBUG
    mongo_connection_string = 'mongodb://localhost:27017/'

# Устанавливаем уровень логирования
logging.basicConfig(level=log_level)

# Подключаемся к MongoDB
client = MongoClient(mongo_connection_string, serverSelectionTimeoutMS=2000)
db = client.messages  # Выбор базы данных "messages"


# logging.info("MongoDB connected at {}: {}".format(client.HOST, client.PORT))

# Модель данных
class Message(BaseModel):
    id: ObjectId = Field(default=None, exclude=True, alias="_id")
    content: str
    host: str = Field(default=None)
    username: str = Field(default=None)

    # Разрешить использование произвольных типов в модели
    class Config:
        arbitrary_types_allowed = True


@app.get("/api/v1/messages/", response_model=list[Message])
def get_messages():
    """Получение всех сообщений"""
    try:
        messages = list(db.messages.find())
        return messages
    except errors.PyMongoError as e:
        logging.error("Error retrieving messages: {}".format(e))
        raise HTTPException(status_code=500, detail="Database error")


@app.post("/api/v1/messages/", response_model=Message)
def create_message(message: Message, request: Request):
    """Создание сообщения в БД"""
    try:
        message_dict = message.dict()
        message_dict["host"] = request.client.host
        db.messages.insert_one(message_dict)
        return message_dict
    except errors.PyMongoError as e:
        logging.error("Error inserting message: {}".format(e))
        raise HTTPException(status_code=500, detail="Database error")


# Запуск приложения
if __name__ == "__main__":
    uvicorn.run(app)
