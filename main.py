
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient

from routes.UserController import User_router
from routes.OpartionController import Operation_router
from routes.VisualizationController import visualization_router
# from pymongo import MongoClient

app = FastAPI()
app.include_router(User_router, prefix="/user")
app.include_router(Operation_router, prefix="/operation")
app.include_router(visualization_router, prefix="/visualization")


client = MongoClient("mongodb://localhost:27017/")


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8002)

