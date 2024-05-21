import datetime
from enum import Enum
from services import OperationService
from services import UserService


from pydantic import BaseModel, ValidationError, Field, validator, field_validator

operation_type = Enum('operation_type', ['EXPENSE', 'REVENUE'])


class Operation(BaseModel):
    id: int
    type: operation_type
    sum: float
    datetime: datetime.datetime
    userId: int

    @field_validator('sum')
    def validate_sum(cls, value):
        if value < 0:
            raise ValueError('Sum is negative')
        return value

    @field_validator('userId')
    async def validate_id(cls, value):
        if_exists = await UserService.if_user_exist(value)
        if not if_exists:
            raise ValueError('User does not exist')
        return value


    class Config:
        arbitrary_types_allowed = True
