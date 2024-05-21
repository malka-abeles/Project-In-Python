from pydantic import BaseModel, constr


class User(BaseModel):
    name: constr(min_length=5, max_length=20)
    id: int
    password: constr(max_length=20, min_length=8)
