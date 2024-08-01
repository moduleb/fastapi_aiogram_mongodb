import os
from dataclasses import dataclass, field

from environs import Env

env = Env()
env.read_env()

# Настройки Redis
@dataclass
class RedisConfig:
    HOST: str = 'localhost'
    PORT: int = 6379

# Настройки логгера
@dataclass
class LoggerConfig:
    LOGFILE: str = 'log.log'
    CLEAR_PERIOD_DAYS: int = 30
    LOG_IN_FILE: bool = False
    LEVEL: str = "DEBUG"
    # LEVEL: str = "INFO"
    # LEVEL: str = "WARN"
    # LEVEL: str = "CRITICAL"
    # LEVEL: str = "ERROR"


# Настройки хеширования пароля
@dataclass
class PasswordHashConfig:
    SALT: bytes = env.str("PWD_SALT").encode('utf-8')
    ITERATIONS: int = env.int("PWD_ITERATIONS")
    ALGORITHM: str = env.str("PWD_ALGORITHM")


# Настройки генерации токена
@dataclass
class TokenConfig:
    # Время жизни токена
    EXPIRATION_TIME_MINUTES: int = 999999999
    SECRET: str = env.str("JWT_SECRET")
    ALGORITHM: str = env.str("JWT_ALGORITHM")


# Настройки базы данных
@dataclass
class DatabaseConfig:
    user: str = "postgres"
    password: str = "postgres"
    host: str = "localhost"
    port: int = 5432
    name: str = "postgres"


# Создание базового config класса
@dataclass
class BaseConfig:
    logger: LoggerConfig = field(default_factory=LoggerConfig)
    password: PasswordHashConfig = field(default_factory=PasswordHashConfig)
    token: TokenConfig = field(default_factory=TokenConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    redis: RedisConfig = field(default_factory=RedisConfig)


# Настройки конфигурации для продакшена
@dataclass
class ProdConfig(BaseConfig):
    database: DatabaseConfig = field(default_factory=lambda: DatabaseConfig(
        user="gooddelo",
        password="gooddelo",
        host="pg",
        name="gooddelo"))
    logger: LoggerConfig = field(default_factory=lambda: LoggerConfig(
        LEVEL="ERROR"))
    redis: RedisConfig = field(default_factory=lambda: RedisConfig(
        HOST="redis"))


# Используем конфигурацию production если передана соответствующая переменная
# устанавливается обычно в файле Docker при сборке контейнера
if os.environ.get("FASTAPI_ENV") == "production":
    config = ProdConfig()
else:
    config = BaseConfig()
