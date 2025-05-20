from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.DBManager import DBManager
from app.migration.migrate import registerUser
from app.auth.auth_handler import signJWT, jwtVerify

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

@app.post("/register", tags=["register user"])
async def register(user: dict) -> dict:
    global db 
    username, password = user['username'], user['password']
    users = await DBManager.getUser(db, username)
    if(len(users) > 0):
        raise HTTPException(status_code=101, detail="Username already exists")
    encrypted = DBManager.encryptPassword(password = password)
    res = await registerUser(db, username = username, password = encrypted)
    return {
        "res": res
    }

@app.post("/login", tags=["login user"])
async def login(user:dict) -> dict:
    global db 
    username, password = user['username'], user['password']
    users = await DBManager.getUser(db, username)
    if(len(users) == 0):
        raise HTTPException(status_code=101, detail="User does not exist")
    encrypted = DBManager.encryptPassword(password = password)
    if(encrypted != users[0].password):
        raise HTTPException(status_code=101, detail="Password is incorrect")
    res = signJWT(users[0].username)
    return {
        "auth_token": res
    }
