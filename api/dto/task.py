import decimal
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, validator


# Модель вывода Task
class ShowTask(BaseModel):
    id: int
    name: str
    price: Decimal
    creation_date: datetime

    # Включение сериализации моделей SQLAlchemy
    class Config:
        orm_mode = True


# Модель вывода Task
class TaskDTO(BaseModel):
    name: str
    price: Decimal

    @validator('name')
    def validate_username(cls, name):

        # Cет разрешенных символов
        allowed_symbols = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя-_ abcdefghijklmnopqrstuvwxyz0123456789")

        # Проверка на пустое значение
        if name is None:
            raise ValueError('Name не может быть пустым')

        # Проверка на длину
        if len(name) < 1 or len(name) > 50:
            raise ValueError('Name должно содержать от 1 до 50 символов')

        # True, если все символы из name есть в allowed_symbols
        if not set(name.lower()).issubset(allowed_symbols):
            raise ValueError('Name содержит недопустимые символы')

        return name

    @validator('price')
    def validate_password(cls, price):

        # Проверка на пустое значение
        if price is None:
            return

        # Проверка, что price - число
        try:
            price = decimal.Decimal(price)
        except decimal.InvalidOperation:
            raise ValueError('Price должен быть числом')

        # Проверка на максимальное значение
        if price > 99999999:
            raise ValueError("Значение 'price' слишком большое")

        return price
