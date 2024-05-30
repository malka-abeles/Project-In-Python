from enum import Enum
# from services import OperationService
from services import UserService
from datetime import datetime
from pydantic import BaseModel, field_validator


# operation_type = Enum('operation_type', ['EXPENSE', 'REVENUE'])
class OperationType(str, Enum):
    EXPENSE = 'EXPENSE'
    REVENUE = 'REVENUE'


class Operation(BaseModel):
    id: int
    type: OperationType
    sum: float
    datetime: datetime
    userId: int

    @field_validator('sum')
    def validate_sum(cls, value):
        if value < 0:
            raise ValueError('Sum is negative')
        return value

    @field_validator('userId', mode='before')
    def validate_id(cls, value):
        if_exists = UserService.if_user_exist(value)
        if not if_exists:
            raise ValueError('User does not exist')
        return value

    class Config:
        arbitrary_types_allowed = True
