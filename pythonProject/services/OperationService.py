from datetime import datetime

from pymongo import DESCENDING

from models.Operation import Operation
from services.dbService import operations


async def create(operation: Operation):
    operation_id = await get_new_operation_id()
    new_operation = operations.insert_one({
        "id": operation_id,
        "type": operation.type.value,
        "sum": operation.sum,
        "datetime": datetime.now(),
        "userId": operation.userId})
    if new_operation:
        return True
    return False


async def update(operation_id: int, operation: Operation):
    await operations.update_one({"id": operation_id},
                                {"$set": {"type": operation.type,
                                          "sum": operation.sum,
                                          "datetime": operation.datetime,
                                          "userId": operation.userId, }})
    operation_update = operations.find_one({"id": operation.id,
                                            "type": operation.type,
                                            "sum": operation.sum,
                                            "datetime": operation.datetime,
                                            "userId": operation.userId,
                                            })
    if operation_update:
        return True
    return False


async def delete(operation_id: int):
    if_delete = operations.delete_one({"id": operation_id})
    if if_delete:
        return True
    return False


async def get_operation_by_id(operation_id: int):
    operation = await  operations.find_one({"id": operation_id})
    return Operation(**operation)


async def get_all_operations_by_user_id(user_id: int):
    all_operations = await operations.find({"userId": user_id})
    operations_list = list(all_operations)
    return operations_list


async def get_operations_between_two_dates_for_user(user_id: int, from_date: str, to_date: str):
    start_date_time = datetime.strptime(from_date, "%Y-%m-%d")
    end_date_time = datetime.strptime(to_date, "%Y-%m-%d")
    result = operations.find({"userId": user_id, "datetime": {"$gte": start_date_time, "$lte": end_date_time}})
    return result


async def get_new_operation_id():
    max_id_operation = await operations.find_one({}, sort=[("id", DESCENDING)])
    print(max_id_operation)
    if max_id_operation:
        return max_id_operation["id"] + 1
    else:
        return 1
