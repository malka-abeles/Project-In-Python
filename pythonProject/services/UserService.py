from pymongo import DESCENDING

from models.User import User
from services.dbService import operations


async def creat(user: User):
    existing_user = operations.find_one({"name": user.name, "password": user.password})
    if existing_user:
        return True
    return False


async def signup(new_user: User):
    user_id = await get_user_id()
    operations.insert_one({
        "id": user_id,
        "name": new_user.name,
        "password": new_user.password
    })
    new_user_created = operations.find_one({"id": user_id})
    if new_user_created:
        return True
    return False


async def update_user_profile(user_id: int, user: User):
    operations.update_one({"id": user_id}, {"$set": {"name": user.name, "password": user.password}})
    user_updated = operations.find_one({"id": user_id, "name": user.name, "password": user.password})
    if user_updated:
        return True
    return False


async def get_user_id():
    max_id_user = operations.find_one({}, sort=[("id", DESCENDING)])
    print(max_id_user)
    if max_id_user:
        return max_id_user["id"] + 1
    else:
        return 1
