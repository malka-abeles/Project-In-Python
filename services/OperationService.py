from datetime import datetime
from pymongo import DESCENDING

from models.Operation import Operation
from services.dbService import operations


async def create(operation: Operation):
    operation_id = await get_new_operation_id()
    new_operation = await operations.insert_one({
        "id": operation_id,
        "type": operation.type.value,
        "sum": operation.sum,
        "datetime": datetime.today(),
        "userId": operation.userId})
    if new_operation:
        return operation_id
    return False


async def update(operation_id: int, operation: Operation):
    await operations.update_one({"id": operation_id},
                                {"$set": {"type": operation.type.value,
                                          "sum": operation.sum,
                                          "datetime": operation.datetime,
                                          "userId": operation.userId, }})
    operation_update = operations.find_one({"id": operation.id,
                                            "type": operation.type.value,
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
    operation = await operations.find_one({"id": operation_id})
    return Operation(**operation) if operation else None


async def get_all_operations_by_user_id(user_id: int):
    all_operations = operations.find({"userId": user_id})
    operations_list = await all_operations.to_list(None)
    return operations_list if operations_list else []


async def get_operations_between_two_dates_for_user(user_id: int, from_date: datetime, to_date: datetime):
    # start_date_time = datetime.strptime(from_date, "%Y-%m-%d")
    # end_date_time = datetime.strptime(to_date, "%Y-%m-%d")
    result = operations.find({"userId": user_id, "datetime": {"$gte": from_date, "$lte": to_date}})
    result_list = await result.to_list(None)
    return result_list


async def get_new_operation_id():
    max_id_operation = await operations.find_one({}, sort=[("id", DESCENDING)])
    if max_id_operation:
        return max_id_operation["id"] + 1
    else:
        return 1
