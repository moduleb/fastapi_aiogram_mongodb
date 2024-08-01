from typing import Type

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.logger import logger
from api.models.task import Task

# Тексты ошибок
read_err = "Ошибка получения информации из базы данных"
create_err = "Ошибка сохранения информации в базу данных"
update_err = "Ошибка обновления информации в базе данных"
delete_err = "Ошибка удаления информации из базы данных"
duplicate_err = "Ошибка сохранения в базу данных: запись уже существует"


class TaskDAO:
    """
    Класс для работы с объектами Task
    """

    @staticmethod
    def create(new_task: Task, session: Session) -> Task:
        """
        Добавляет новый task в базу данных.
        """
        try:
            # Создание нового task и сохранение изменений в базе данных
            session.add(new_task)
            session.commit()
            logger.debug(f"Сохранено в db: {new_task}")

        except IntegrityError as e:
            # Если уже существует
            if 'already exists' in str(e):
                logger.debug(f"Already exists: {new_task}")
                raise HTTPException(500, detail=duplicate_err)

        except Exception as e:
            # Если произошла какая-либо другая ошибка
            logger.error(f"{create_err}: {e}")
            raise HTTPException(500, detail=create_err)

        else:
            # Если ошибок не возникло, возвращаем созданный task
            return new_task

    @staticmethod
    def get_one(task_id: int, session: Session) -> Task:
        """
        Извлекает task с заданным id из базы данных.
        """
        try:
            task = session.query(Task).filter(Task.id == task_id).first()
            logger.debug(f"Получено из db: {task}")
            return task

        except Exception as e:
            logger.error(f"{read_err}: {e}")
            raise HTTPException(500, detail=read_err)

    @staticmethod
    def get_all(session: Session) -> list[Type[Task]]:
        """
        Извлекает все объекты task из базы данных.
        """
        try:
            tasks = session.query(Task).all()
            logger.debug(f"Получено из db: {tasks}")
            return tasks


        except Exception as e:
            logger.error(f"{read_err}: {e}")
            raise HTTPException(500, detail=read_err)

    @staticmethod
    def update(task: Task, session: Session) -> Task:
        """
        Обновляет task в базе данных.
        """
        try:
            # Обновление task и сохранение изменений в базе данных
            session.add(task)
            session.commit()
            logger.debug(f"Сохранено в db: {task}")

        except IntegrityError as e:
            # Если уже существует
            if 'already exists' in str(e):
                logger.debug(f"Already exists: {task}")
                raise HTTPException(500, detail=duplicate_err)

        except Exception as e:
            logger.error(f"{update_err}: {e}")
            raise HTTPException(500, detail=update_err)

        else:
            # Если ошибок не возникло, возвращаем обновленный task
            return task

    @staticmethod
    def delete(task: Task, session: Session):
        """
        Удаляет task из базы данных.
        """
        try:
            session.delete(task)
            session.commit()
            logger.debug(f"Удалено из db: {task}")

        except Exception as e:
            logger.error(f"{delete_err}: {e}")
            raise HTTPException(500, detail=delete_err)
