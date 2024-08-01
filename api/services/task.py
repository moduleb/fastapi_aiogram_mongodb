
from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.dao.task import TaskDAO
from api.dto.task import TaskDTO
from api.models.task import Task


class TaskService:
    def __init__(self, dao: TaskDAO):
        self.dao = dao

    def create(self, data: TaskDTO, session: Session) -> Task:
        """
        Создает новый объект task и сохраняет его в базу данных.
        """
        # Создаем новый объект Task
        new_task = Task(**data.dict())

        # Сохраняем в базу данных и возвращаем объект task
        return self.dao.create(new_task, session)

    def get_all(self, session: Session) -> list[Type[Task]]:
        """
        Получаем все объекты task из базы данных
        """
        return self.dao.get_all(session)

    def get_one(self, task_id: int, session: Session) -> Task:
        """
        Получаем объект Task по id из базы данных
        """
        task = self.dao.get_one(task_id, session)
        if not task:
            raise HTTPException(404, detail="Task не найден")
        return task

    def update(self, task_id: int, data: TaskDTO, session: Session) -> Task:
        """
        Обновляем объект task в базе данных
        """

        # Получаем task из базы данных
        task = self.get_one(task_id, session)

        # Если поле name задано - обновляем
        if data.name:
            task.name = data.name

        # Если поле price задано - обновляем
        if data.price:
            task.price = data.price

        return self.dao.update(task, session)

    def delete(self, task_id: int, session: Session) -> None:
        """
        Удаляет объект task из базы данных
        """
        task = self.get_one(task_id, session)

        self.dao.delete(task, session)
