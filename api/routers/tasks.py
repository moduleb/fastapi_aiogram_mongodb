from typing import List

from fastapi import APIRouter, Depends, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.params import Body
from sqlalchemy.orm import Session

from api.container import task_service, auth_service
from api.database import get_session
from api.dto.task import ShowTask, TaskDTO
from api.limiter import limiter

router = APIRouter()


# """CREATE TASK"""
@router.post("/", response_model=ShowTask,
             summary="Create Task",
             description=" - Возвращает JSON с информацией о созданной записи 'task'\n"
                         " - Требует наличия токена в заголовке запроса в поле 'Authorization'")
@limiter.limit("5/minute")
async def create(request: Request,
                 data: TaskDTO,
                 current_username: str = Depends(auth_service.verify_token),
                 session: Session = Depends(get_session)):
    return task_service.create(data, session)


# """GET ALL TASKS"""
@router.get("/", response_model=List[ShowTask],
            summary="Get all tasks'",
            description=" - Возвращает JSON с информацией обо всех записях 'task'\n"
                        " - Требует наличия токена в заголовке запроса в поле 'Authorization'")
@limiter.limit("5/minute")
async def get_all(request: Request,
                  session: Session = Depends(get_session),
                  current_username: str = Depends(auth_service.verify_token)):
    return jsonable_encoder(task_service.get_all(session))


# """GET TASK BY ID"""
@router.get("/{task_id}", response_model=ShowTask,
            summary="Get task by ID'",
            description=" - Возвращает JSON с информацией о найденной по id записи 'task'\n"
                        " - Требует наличия токена в заголовке запроса в поле 'Authorization'")
@limiter.limit("5/minute")
async def get_one(request: Request,
                  task_id: int,
                  current_username: str = Depends(auth_service.verify_token),
                  session: Session = Depends(get_session)):
    return task_service.get_one(task_id, session)


# """UPDATE TASK"""
@router.put("/{task_id}", response_model=ShowTask,
            summary="Update task'",
            description=" - Возвращает JSON с информацией о найденной по id записи 'task'\n"
                        " - Требует наличия токена в заголовке запроса в поле 'Authorization'")
@limiter.limit("5/minute")
async def update(request: Request,
                 task_id: int,
                 data: TaskDTO,
                 current_username: str = Depends(auth_service.verify_token),
                 session: Session = Depends(get_session)):
    return task_service.update(task_id, data, session)



# """DELETE TASK"""
@router.delete("/{task_id}",
               summary="Delete task'",
               description=" - Возвращает JSON с информацией о найденной по id записи 'task'\n"
                           " - Требует наличия токена в заголовке запроса в поле 'Authorization'")
@limiter.limit("5/minute")
async def delete(request: Request,
                 task_id: int,
                 current_username: str = Depends(auth_service.verify_token),
                 session: Session = Depends(get_session)):
    task_service.delete(task_id, session)

    return Response(status_code=204)
