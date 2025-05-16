from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db import database

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3000/"
]

db = database()

@asynccontextmanager
async def lifespan(app):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

backPref = "Japanese anime song"


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to this amazing project."}

# @app.get("/ytMusicSearch", tags=["music search"])
# async def getYTResults() -> dict:
#     # res = query(backPref)
#     # return { "result": res}
#     return []

@app.post("/pref", tags=["preference"])
async def set_pref(request) -> dict:
    global backPref 
    backPref= request.query
    return {
        "data": f"Successfully received: {request.query}"
    }

@app.get("/dbtest", tags=["db test"])
async def dbtest() -> dict:
    global db
    context = "SELECT * FROM musicdata LIMIT 1;"
    res = await db.query(context)
    return {
        "result": res
    }

