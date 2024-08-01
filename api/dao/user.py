from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.logger import logger
from api.models.user import User

# Тексты ошибок
read_err = "Ошибка получения информации из базы данных"
create_err = "Ошибка сохранения информации в базу данных"
update_err = "Ошибка обновления информации в базе данных"
delete_err = "Ошибка удаления информации из базы данных"
duplicate_err = "Ошибка сохранения в базу данных: запись уже существует"


class UserDAO:
    """
    Класс для работы с объектами User
    """
    @staticmethod
    def create_user(new_user: User, session: Session) -> User:
        """
        Добавляет нового пользователя в базу данных.
        """
        try:
            # Добавление нового пользователя и сохранение изменений в базе данных
            session.add(new_user)
            session.commit()
            logger.debug(f"Сохранено в db: {new_user}")

        except IntegrityError as e:
            # Если произошла ошибка целостности (дублирование)
            if 'already exists' in str(e):
                logger.debug(f"Already exists: {new_user}")
                raise HTTPException(500, detail=duplicate_err)

        except Exception as e:
            # Если произошла какая-либо другая ошибка
            logger.error(f"{create_err}: {e}")
            raise HTTPException(500, detail=create_err)

        else:
            # Если ошибок не возникло, возвращаем созданного пользователя
            return new_user

    @staticmethod
    def get_user(username: str, session: Session) -> User:
        """
        Извлекает пользователя с заданным именем пользователя из базы данных.
        """
        try:
            # Выполнение запроса к базе данных для поиска пользователя с заданным именем пользователя
            user = session.query(User).filter(User.username == username).first()
            logger.debug(f"Получено из db: {user}")
            return user

        except Exception as e:
            logger.error(f"{read_err}: {e}")
            raise HTTPException(500, detail=read_err)
