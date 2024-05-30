import asyncio

import pytest
from datetime import datetime, timedelta

from pymongo import DESCENDING
from services import OperationService, UserService, dbService
from models.Operation import Operation, OperationType

new_operation_id = None


@pytest.fixture
def operation_data():
    return Operation(id=30, type=OperationType.EXPENSE, sum=100.0, datetime=datetime.now(), userId=5)


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_create(operation_data):
    global new_operation_id
    result = await OperationService.create(operation_data)
    assert result is not False
    new_operation_id = result
    updated_operation = await dbService.operations.find_one({"id": operation_data.id})
    assert updated_operation is not None


@pytest.mark.asyncio
async def test_add_operation_not_valid_sum(operation_data):
    with pytest.raises(ValueError, match='Sum is negative'):
        Operation(id=30, type=OperationType.EXPENSE, sum=-100.0, datetime=datetime.now(), userId=5)


# @pytest.mark.asyncio
# async def test_add_operation_not_valid_user_id():
#     max_id_operation = await dbService.operations.find_one({}, sort=[("id", DESCENDING)])
#     with pytest.raises(ValueError, match='User does not exist'):
#         Operation(id=30, type=OperationType.EXPENSE, sum=100.0, datetime=datetime.now(), userId=max_id_operation['id']+1)

@pytest.mark.asyncio
async def test_get_operation_by_id(operation_data):
    result = await OperationService.get_operation_by_id(operation_data.id)
    assert result is not None
    # for field in vars(operation_data).keys():
    #     if field != "datetime":
    #         assert vars(result)[field] == vars(operation_data)[field], f"Mismatch in field '{field}'"


@pytest.mark.asyncio
async def test_get_all_operations_by_user_id(operation_data):
    list_result = await dbService.operations.find({"userId": operation_data.userId}).to_list(None)
    result = await OperationService.get_all_operations_by_user_id(operation_data.userId)
    assert len(result) == len(list_result)
    for op1, op2 in zip(result, list_result):
        for field in op1.keys():
            if field != 'datetime':
                assert op1[field] == op2[field]


@pytest.mark.asyncio
async def test_get_operations_between_two_dates_for_user(operation_data):
    start_date_time = datetime.now() - timedelta(days=30)
    end_date_time = datetime.now()
    list_result = await dbService.operations.find(
        {"userId": operation_data.userId, "datetime": {"$gte": start_date_time, "$lte": end_date_time}}).to_list(None)
    result = await OperationService.get_operations_between_two_dates_for_user(operation_data.userId, start_date_time,
                                                                              end_date_time)
    for op1, op2 in zip(result, list_result):
        for field in op1.keys():
            if field not in ['_id', 'datetime']:
                assert op1[field] == op2[field]


@pytest.mark.asyncio
async def test_update(operation_data):
    global new_operation_id
    operation_data.sum = 150.0
    result = await OperationService.update(new_operation_id, operation_data)
    assert result is True
    updated_operation = await dbService.operations.find_one({"id": new_operation_id})
    assert updated_operation is not None
    assert updated_operation['sum'] == operation_data.sum
    operation_data.sum = 100.0
    await OperationService.update(new_operation_id, operation_data)


@pytest.mark.asyncio
async def test_update_operation_not_valid_sum():
    with pytest.raises(ValueError, match='Sum is negative'):
        Operation(id=30, type=OperationType.EXPENSE, sum=-100.0, datetime=datetime.now(), userId=5)


# @pytest.mark.asyncio
# async def test_update_operation_not_valid_user_id():
#     max_id_operation = await dbService.operations.find_one({}, sort=[("id", DESCENDING)])
#     with pytest.raises(ValueError, match='User does not exist'):
#         Operation(id=30, type=OperationType.EXPENSE, sum=100.0, datetime=datetime.now(), userId=max_id_operation['id']+1000000)


@pytest.mark.asyncio
async def test_delete():
    result = await OperationService.delete(1)
    assert result is True


@pytest.mark.asyncio
async def test_get_new_operation_id(operation_data):
    max_id_operation = await dbService.operations.find_one({}, sort=[("id", DESCENDING)])
    num = await OperationService.get_new_operation_id()
    if max_id_operation is None:
        assert int(num) is int(1)
    else:
        assert num is max_id_operation['id'] + 1
