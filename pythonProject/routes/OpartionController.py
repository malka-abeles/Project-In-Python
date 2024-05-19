from fastapi import FastAPI, Depends, APIRouter, HTTPException

from services import OperationService
from models.Operation import Operation
from typing import List

Operation_router = APIRouter()


# @router.post("/")
# async def signin(user: User):
#     is_sign_in = await UserService.signin(user)
#     if is_sign_in:
#         return "you were signed in successfully"
#     raise HTTPException(status_code=404, detail="this user is not exist")
#
#
# @router.put("/")
# async def signup(user: User):
#     is_sign_up =await UserService.signup(user)
#     if is_sign_up:
#         return "you were signed up successfully"
#     raise HTTPException(status_code=400, detail="one or more of your details was not valid, please try again")
#
#
# @router.put("/setProfile/{id}")
# async def update_profile(user_id: int, user: User):
#     is_updated = await UserService.update_user_profile(user_id, user)
#     if is_updated:
#         return "your profile were updated successfully"
#     raise HTTPException(status_code=400, detail="one or more of your details was not valid, please try again")


@Operation_router.put("/update")
async def update_operation(operation_id: int, operation: Operation):
    is_update = await OperationService.update(operation_id, operation)
    if is_update:
        return operation
    else:
        raise HTTPException(status_code=404, detail="Operation not found")


@Operation_router.delete("/delete")
async def delete_operation(operation_id: int, operation: Operation):
    is_delete = await OperationService.delete(operation_id)
    if is_delete:
        return operation
    else:
        raise HTTPException(status_code=404, detail="Operation not found")


@Operation_router.get("/getTerm", response_model=List[Operation])
async def get_operation(user_id: int, from_date: str, to_date: str):
    operation = await OperationService.get_operations_between_two_dates_for_user(user_id, from_date, to_date)
    aaa = [Operation(**doc) for doc in operation]
    return aaa


@Operation_router.get("/getUserId", response_model=List[Operation])
async def get_operation(user_id: int):
    operation = await OperationService.get_all_operations_by_user_id(user_id)
    aaa = [Operation(**doc) for doc in operation]
    return aaa


@Operation_router.post("/create")
async def create_operation(operation: Operation):
    is_create = await OperationService.create(operation)
    if is_create:
        return "nn"
    else:
        raise HTTPException(status_code=404, detail="Operation not found")
