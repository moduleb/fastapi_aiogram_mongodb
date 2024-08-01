from typing import List

from fastapi import HTTPException

from api.logger import logger
from redis_ import r

REDIS_ERROR_MSG = "Redis недоступен"


class RedisDAO:
    """
    Класс для работы с хранилищем Redis
    """
    @staticmethod
    def add_token(username: str, token: str) -> None:
        # Добавление токена в список деактивированных токенов пользователя
        try:
            result = r.rpush(username, token)
            logger.debug(f"Добавление токена в список деактивированных: {result}")
        except Exception as e:
            logger.error(f"{REDIS_ERROR_MSG} {e}")
            raise HTTPException(status_code=500, detail=REDIS_ERROR_MSG)

    @staticmethod
    def check_token(username: str, token: str) -> bool:
        # Проверка наличия токена в списке деактивированных токенов пользователя
        try:
            tokens: List[bytes] = r.lrange(username, 0, -1)
            result = token.encode('utf-8') in tokens
            logger.debug(f"Проверка наличия токена в списке деактивированных: {result}")
            return result
        except Exception as e:
            logger.error(f"{REDIS_ERROR_MSG} {e}")
            raise HTTPException(status_code=500, detail=REDIS_ERROR_MSG)

