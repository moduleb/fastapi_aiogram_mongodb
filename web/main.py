import logging
import os
import uvicorn
from bson import ObjectId
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymongo import MongoClient, errors

# Проверяем, запущено ли приложение в докере
is_running_in_docker = os.path.exists('/.dockerenv') or os.path.exists('/proc/1/cgroup')

# Создаем приложение FastAPI
app = FastAPI()

# Устанавливаем строку подключения к MongoDB и
# уровень логирования в зависимости от окружения.
if is_running_in_docker:
    mongo_connection_string = "mongodb://mongo:27017/"
    log_level = logging.INFO
else:
    log_level = logging.DEBUG
    mongo_connection_string = 'mongodb://localhost:27017/'

# Устанавливаем уровень логирования
logging.basicConfig(level=log_level)

# Подключаемся к MongoDB
try:
    client = MongoClient(mongo_connection_string, serverSelectionTimeoutMS=2000)
    client.admin.command('ping')  # Это вызовет ошибку, если MongoDB недоступна
    db = client.messages  # Выбор базы данных "messages"
    logging.info("MongoDB connected at {}: {}".format(client.HOST, client.PORT))
except Exception as e:
    logging.error("Could not connect to MongoDB:\n{}".format(e))
    raise SystemExit("Exiting due to MongoDB connection error.")


# Модель данных
class Message(BaseModel):
    id: ObjectId = Field(default=None, exclude=True, alias="_id")
    content: str

    # Разрешить использование произвольных типов в модели
    class Config:
        arbitrary_types_allowed = True


# Получение всех сообщений
@app.get("/api/v1/messages/", response_model=list[Message])
def get_messages():
    try:
        messages = list(db.messages.find())
        return messages
    except errors.PyMongoError as e:
        logging.error("Error retrieving messages: {}".format(e))
        raise HTTPException(status_code=500, detail="Database error")


# Создание сообщения в БД
@app.post("/api/v1/messages/", response_model=Message)
def create_message(message: Message):
    try:
        message_dict = message.dict()
        db.messages.insert_one(message_dict)
        return message_dict
    except errors.PyMongoError as e:
        logging.error("Error inserting message: {}".format(e))
        raise HTTPException(status_code=500, detail="Database error")

# Запуск приложения
if __name__ == "__main__":
    uvicorn.run(app)
