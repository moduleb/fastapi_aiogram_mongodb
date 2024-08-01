import uvicorn
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from api.limiter import limiter
from api.routers import tasks, login, register, logout

# Создаем приложение
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Регистрируем эндпоинты
app.include_router(register.router, prefix='/register', tags=["/register"])
app.include_router(login.router, prefix='/login', tags=["/login"])
app.include_router(logout.router, prefix='/logout', tags=["/logout"])
app.include_router(tasks.router, prefix='/tasks', tags=["/tasks"])

# Запускаем приложение
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
