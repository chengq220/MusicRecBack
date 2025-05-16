from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db import database
import app.query as qy

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3000/"
]

db = database()

@asynccontextmanager
async def lifespan(app):
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

@app.post("/pref", tags=["preference"])
async def set_pref(request) -> dict:
    global backPref 
    backPref= request.query
    return {
        "data": f"Successfully received: {request.query}"
    }

@app.get("/query", tags=["db query item"])
async def dbtest() -> dict:
    global db
    context = "SELECT * FROM musicdata LIMIT 10;"
    res = await qy.execContext(db, context)
    return {
        "result": res
    }

