from idlelib.iomenu import errors

from pymongo import DESCENDING
from models.User import User
from services.dbService import synchronise_users, users


async def sign_in(user: User):
    existing_user = await users.find_one({"name": user.name, "password": user.password})
    if not existing_user:
        raise errors.UserDoesNotExist
    else:
        return existing_user is not None


async def sign_up(new_user: User):
    user_id = await get_user_id()
    await users.insert_one({
        "id": user_id,
        "name": new_user.name,
        "password": new_user.password
    })
    new_user_created = await users.find_one({"id": user_id})
    return user_id if new_user_created else False


async def update_user_profile(user_id: int, user: User):
    await users.update_one({"id": user_id}, {"$set": {"name": user.name, "password": user.password}})
    user_updated = await users.find_one({"id": user_id})
    return user_updated is not None


async def get_user_id():
    max_id_user = await users.find_one({}, sort=[("id", DESCENDING)])
    return max_id_user["id"] + 1 if max_id_user else 1


def if_user_exist(id1: int):
    result = synchronise_users.find_one({"id": id1})
    if result is None:
        return False
    return True
