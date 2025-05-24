from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.DBManager import DBManager
import app.migration.migrate as mm
from app.auth.auth_handler import signJWT, jwtVerify
import app.db.query as dbq
import random 

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("error.log"),  # Save to file
        logging.StreamHandler()           # Also print to console (optional)
    ]
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3000/"
]

db = DBManager()

@asynccontextmanager
async def lifespan(app):
    global db
    await db.connect()
    yield
    await db.disconnect()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to this amazing project."}

@app.post("/register", tags=["Authentication"])
async def register(user: dict) -> dict:
    global db 
    username, password = user['username'], user['password']
    users = await DBManager.getUser(db, username)
    if(len(users) > 0):
        raise HTTPException(status_code=101, detail="Username already exists")
    encrypted = DBManager.encryptPassword(password = password)
    res = await mm.registerUser(db, username = username, password = encrypted)
    return {
        "res": res
    }

@app.post("/login", tags=["Authentication"])
async def login(user:dict) -> dict:
    global db 
    username, password = user['username'], user['password']
    users = await DBManager.getUser(db, username)
    if(len(users) == 0):
        raise HTTPException(status_code=101, detail="User does not exist")
    encrypted = DBManager.encryptPassword(password = password)
    if(encrypted != users[0].password):
        raise HTTPException(status_code=101, detail="Password is incorrect")
    userInfo = {
        "username": users[0].username,
        "new_user": users[0].new_user
    }
    res = signJWT(userInfo)
    return {
        "auth_token": res
    }

@app.post("/updatePref", tags=["User Preference"])
async def updatePref(pref: dict) -> dict:
    global db 
    user, artist, genre = pref['user'], pref['artist'], pref['genre']
    res = await mm.updateUserPreference(db, user = user, artist = artist, genre = genre)
    return {
        "res": res
    }

@app.post("/getPref", tags=["User Preference"])
async def getPref(user: dict) -> dict:
    global db 
    user = user["user"]
    res = await dbq.getPref(db, user = user)
    return {
        "res": res
    }

# @app.post("/decodeToken", tags = ["decode token"])
# async def decodeToken(inp:dict) -> dict:
#     print("im getting called")
#     with open("output.txt", "w") as file:
#         file.write(f"token: {inp["token"]}")
#     return jwtVerify(inp["token"])

@app.post("/getMusic", tags=["Music"])
async def getMusic(userInfo:dict) -> dict:
    global db 
    NUM_DESIRE = 20
    size = await dbq.getTableSize(db, "musicdata")
    lb = random.randint(1, size - NUM_DESIRE)
    ub = lb + NUM_DESIRE
    res = await dbq.getMusicBetweenIndices(db, lb, ub)
    return {
        "result": res
    }
