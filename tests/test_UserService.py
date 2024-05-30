# import pytest
# from models.User import User
# from services import dbService, UserService
# from pymongo import DESCENDING
# import asyncio
#
#
#
# @pytest.fixture
# def user_data():
#     return User(name="malka", id=0, password="abcdefgh")
#
#
# @pytest.fixture(scope="module")
# def event_loop():
#     loop = asyncio.new_event_loop()
#     yield loop
#     loop.close()
#
#
# @pytest.mark.asyncio
# async def test_sign_in(user_data):
#     existing_user = await dbService.users.find_one({"name": user_data.name, "password": user_data.password})
#     result = await UserService.sign_in(user_data)
#     if existing_user:
#         assert result is True
#     else:
#         assert result is False
#
#
# @pytest.mark.asyncio
# async def test_sign_up(user_data):
#     result = await UserService.sign_up(user_data)
#     assert result is not False
#     user_data.id = result
#     created_operation = await dbService.users.find_one({"id": user_data.id})
#     assert created_operation is not None
#
#
# @pytest.mark.asyncio
# async def test_update_user_profile(user_data):
#     user_data.name = "malka mirym"
#     result = await UserService.update_user_profile(user_data.id, user_data)
#     assert result is True
#     updated_user = await dbService.users.find_one({"id": user_data.id})
#     assert updated_user is not None
#     assert updated_user['name'] == user_data.name
#     user_data.name = "malka"
#     await UserService.update_user_profile(user_data.id, user_data)
#
#
# @pytest.mark.asyncio
# async def test_get_user_id():
#     max_id_user = await dbService.users.find_one({}, sort=[("id", DESCENDING)])
#     num = await UserService.get_user_id()
#     if max_id_user is None:
#         assert num == 1
#     else:
#         assert num == max_id_user['id'] + 1
#
#
# @pytest.mark.asyncio
# async def test_if_user_exist(user_data):
#     if_exist = await dbService.users.find_one({"id": user_data.id})
#     result = await UserService.if_user_exist(user_data.id)
#     assert result == if_exist
#
#
# @pytest.mark.asyncio
# async def test_if_password_exist(user_data):
#     if_exist = await dbService.users.find_one({"password": user_data.password})
#     result = await UserService.if_password_exist(user_data.password)
#     assert result == if_exist


import asyncio
import pytest
from models.User import User
from services import dbService, UserService
from pymongo import DESCENDING

new_user_id = None
my_name: str = "malka"
my_password: str = "passworddd"
my_user: User = User(name=my_name, id=1, password=my_password)


@pytest.fixture
def user_data():
    return User(name="malka", id=1, password="abcdefgh")


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_sign_up():
    global new_user_id
    result = await UserService.sign_up(User(name=my_name, id=1, password=my_password))
    assert result is not False
    new_user_id = result
    created_operation = await dbService.users.find_one({"id": new_user_id})
    assert created_operation is not None


@pytest.mark.asyncio
async def test_sign_up_with_existing_password():
    with pytest.raises(ValueError, match='Password already exist'):
        User(name=my_name, id=1, password=my_password)


@pytest.mark.asyncio
async def test_sign_in():
    existing_user = await dbService.users.find_one({"name": my_name, "password": my_password})
    result = await UserService.sign_in(my_user)
    assert result is (existing_user is not None)


@pytest.mark.asyncio
async def test_sign_in_with_not_existing_user():
    with pytest.raises(Exception):
        # await dbService.users.find_one({"name": "testing", "password": "testing1"})
        await UserService.sign_in(User(name="testing", id=1, password="testing1"))


@pytest.mark.asyncio
async def test_update_user_profile():
    global new_user_id
    # user_data.name = "malka mirym"
    my_user.name = "malka mirym"
    print(f"{new_user_id}{my_name},{my_password}")
    result = await UserService.update_user_profile(new_user_id, my_user)
    assert result is not None
    updated_user = await dbService.users.find_one({"id": new_user_id})
    assert updated_user is not None
    assert updated_user['name'] == my_user.name
    # user_data.name = "malka"
    my_user.name = 'malka'
    await UserService.update_user_profile(new_user_id, my_user)


@pytest.mark.asyncio
async def test_get_user_id():
    max_id_user = await dbService.users.find_one({}, sort=[("id", DESCENDING)])
    num = await UserService.get_user_id()
    if max_id_user is None:
        assert num == 1
    else:
        assert num == max_id_user['id'] + 1


@pytest.mark.asyncio
async def test_if_user_exist():
    if_exist = await dbService.users.find_one({"id": new_user_id})
    result = UserService.if_user_exist(new_user_id)
    print(result)
    if if_exist is None:
        assert result is False
    else:
        assert result is True


@pytest.mark.asyncio
async def test_if_user_not_exist():
    user_exists = UserService.if_user_exist(9999999999999999)
    assert user_exists is False
    await delete_user()


async def delete_user():
    dbService.users.delete_one({"password": my_password})
