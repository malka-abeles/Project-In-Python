from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
db = client["Investors"]

users = db["Users"]
operations = db["Operations"]
