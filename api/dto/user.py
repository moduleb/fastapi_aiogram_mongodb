from pydantic import BaseModel, validator

# Модель валидации объекта User при входе в систему
class UserLoginDTO(BaseModel):
    username: str
    password: str

# Модель валидации объекта User при отправке пользователю
class ShowUser(BaseModel):
    id: int
    username: str

    # Включение сериализации моделей SQLAlchemy
    class Config:
        orm_mode = True

# Модель валидации объекта User при регистрации
class UserDTO(BaseModel):
    username: str
    password: str

    @validator('username')
    def validate_username(cls, v):
        allowed_symbols = set("abcdefghijklmnopqrstuvwxyz-_1234567890")

        # True, если все элементы из v есть в allowed_symbols
        if not set(v.lower()).issubset(allowed_symbols):
            raise ValueError('Username содержит недопустимые символы')

        if len(v) < 3 or len(v) > 16:
            raise ValueError('Username должно содержать от 3 до 16 символов')
        return v


    @validator('password')
    def validate_password(cls, v):

        # Проверка на длину пароля
        if len(v) < 6 or len(v) > 20:
            raise ValueError('Password должен содержать от 6 до 20 символов')

        # Проверка на недопустимые символы
        allowed_symbols = set("!#$%&'()*+,-./:;<=>?@[]^_`{|}~1234567890abcdefghijklmnopqrstuvwxyz")
        if not set(v.lower()).issubset(allowed_symbols):
            raise ValueError('Password содержит недопустимые символы')

        # True, если v и регулярное выражение не имеют общих элементов
        # Проверки, содержит ли пароль английские буквы в нижнем регистре, верхнем и цифры
        error = 'Password должен содержать буквы английского алфавита в нижнем и верхнем регистре и хотя бы одну цифру.'
        if set(v).isdisjoint(set("abcdefghijklmnopqrstuvwxyz")):
            raise ValueError(error)
        if set(v).isdisjoint(set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")):
            raise ValueError(error)
        if set(v).isdisjoint(set("1234567890")):
            raise ValueError(error)

        # Включить, если в пароле должны быть спецсимволы
        # if set(v).isdisjoint(set("!#$%&'()*+,-./:;<=>?@[]^_`{|}~")):
        #     raise ValueError(error)

        return v
