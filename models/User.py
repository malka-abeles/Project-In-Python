from pydantic import BaseModel, constr, field_validator
from services import dbService


class User(BaseModel):
    name: constr(min_length=5, max_length=20)
    id: int
    password: constr(max_length=20, min_length=8)

    @field_validator('password', mode='before')
    def password_validator(cls, value):
        password_exist = if_password_exist(value)
        if password_exist:
            raise ValueError('Password already exist')
        return str(value)


def if_password_exist(password: str):
    if_exist = dbService.synchronise_users.find_one({"password": password})
    return if_exist
