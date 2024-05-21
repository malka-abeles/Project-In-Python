from pymongo import MongoClient

from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client["Investors"]

users = db["Users"]
operations = db["Operations"]
