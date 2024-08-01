from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from api.container import user_service, auth_service
from api.database import get_session
from api.dto.user import UserDTO
from api.limiter import limiter

router = APIRouter()


@router.post("/", summary="Регистрация пользователя",
             description=" - Принимает username и password нового пользователя \n"
                         " - Возвращает токен доступа на 30 минут")
@limiter.limit("5/minute")
async def register(request: Request,
                   data: UserDTO,
                   session: Session = Depends(get_session)):
    # Создаем пользователя
    new_user = user_service.create_user(data, session)

    # Генерируем токен на основе username
    access_token = auth_service.create_access_token(new_user.username)

    # Возвращаем токен
    return {"access_token": access_token, "token_type": "bearer"}
