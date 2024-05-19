import datetime
from enum import Enum
from typing import List


from pydantic import BaseModel

operation_type = Enum('operation_type', ['EXPENSE', 'REVENUE'])


class Operation(BaseModel):
    id: int
    type: operation_type
    sum: float
    datetime: datetime.datetime
    userId: int

    class Config:
        arbitrary_types_allowed = True
