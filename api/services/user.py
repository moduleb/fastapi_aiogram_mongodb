import base64
import hashlib

from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.config import config
from api.dao.user import UserDAO
from api.logger import logger
from api.models.user import User


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def create_user(self, data, session: Session) -> User:
        """
        Создает нового пользователя и сохраняет его в базу данных.
        """
        # Создаем новый объект User
        new_user = User(**data.dict())

        # Записываем хещ пароля
        new_user.password = self.hash_password(data.password)

        # Сохраняем пользователя и возвращаем объект User
        return self.dao.create_user(new_user, session)

    def get_user(self, username: str, session: Session) -> User:
        """
        Получаем объект User по username
        """
        return self.dao.get_user(username, session)

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Хеширует пароль с помощью PBKDF2 и возвращает его в виде строки base64.
        """
        try:
            hash_digest = hashlib.pbkdf2_hmac(
                config.password.ALGORITHM,
                password.encode('utf-8'),
                config.password.SALT,
                config.password.ITERATIONS
            )
            return base64.b64encode(hash_digest).decode('utf-8')

        except Exception as e:
            logger.error(f'Ошибка функции хеширования пароля: {e}')
            raise HTTPException(500, detail="Ошибка функции хеширования пароля")
