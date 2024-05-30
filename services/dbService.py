from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

synchronise_client = MongoClient("mongodb://localhost:27017/")
synchronise_db = synchronise_client["Investors"]
synchronise_users = synchronise_db["Users"]
synchronise_operations = synchronise_db["Operations"]

client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client["Investors"]
users = db["Users"]
operations = db["Operations"]
