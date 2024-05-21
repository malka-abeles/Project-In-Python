from pymongo import DESCENDING

from models.User import User
from services.dbService import users


async def sign_in(user: User):
    existing_user = users.find_one({"name": user.name, "password": user.password})
    if existing_user:
        return True
    return False


async def sign_up(new_user: User):
    user_id = await get_user_id()
    users.insert_one({
        "id": user_id,
        "name": new_user.name,
        "password": new_user.password
    })
    new_user_created = users.find_one({"id": user_id})
    if new_user_created:
        return True
    return False


async def update_user_profile(user_id: int, user: User):
    users.update_one({"id": user_id}, {"$set": {"name": user.name, "password": user.password}})
    user_updated = users.find_one({"id": user_id, "name": user.name, "password": user.password})
    if user_updated:
        return True
    return False


async def get_user_id():
    max_id_user = users.find_one({}, sort=[("id", DESCENDING)])
    if max_id_user:
        return max_id_user["id"] + 1
    else:
        return 1


async def if_user_exist(id: int):
    print("aaaaaaa"+id)
    if_exist =await users.find_one({"id": id})
    print("aaaaaa"+if_exist)
    # , {"_id": 0}
    return if_exist
