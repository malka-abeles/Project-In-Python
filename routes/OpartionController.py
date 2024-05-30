from fastapi import FastAPI, Depends, APIRouter, HTTPException

from services import OperationService
from models.Operation import Operation
from typing import List
from utils.log import log

Operation_router = APIRouter()


@Operation_router.put("/update")
@log
async def update_operation(operation_id: int, operation: Operation):
    is_update = await OperationService.update(operation_id, operation)
    if is_update:
        return "operation were updated successfully"
    else:
        raise HTTPException(status_code=404, detail="Operation not found")


@Operation_router.delete("/delete")
@log
async def delete_operation(operation_id: int):
    is_delete = await OperationService.delete(operation_id)
    if is_delete:
        return
    else:
        raise HTTPException(status_code=404, detail="Operation not found")


@Operation_router.get("/getTerm", response_model=List[Operation])
@log
async def get_operation(user_id: int, from_date: str, to_date: str):
    operation = await OperationService.get_operations_between_two_dates_for_user(user_id, from_date, to_date)
    aaa = [Operation(**doc) for doc in operation]
    return aaa


@Operation_router.get("/getUserId", response_model=List[Operation])
@log
async def get_operation(user_id: int):
    operation = await OperationService.get_all_operations_by_user_id(user_id)
    aaa = [Operation(**doc) for doc in operation]
    return aaa


@Operation_router.post("/create")
@log
async def create_operation(operation: Operation):
    is_create = await OperationService.create(operation)
    if is_create:
        return "operation added successfully"
    raise HTTPException(status_code=404, detail="Operation not found")
