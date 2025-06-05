from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.DBManager import DBManager
import app.migration.migrate as mm
from app.auth.auth_handler import signJWT, jwtVerify
import app.db.query as dbq 
import app.recommendation.rec  as rec
from app.api.spotify import Spotify

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3000/"
]

db = DBManager()
spfy = Spotify()

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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username already exist")
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
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
    encrypted = DBManager.encryptPassword(password = password)
    if(encrypted != users[0].password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Password is incorrect")
    userInfo = {
        "username": users[0].username
    }
    res = signJWT(userInfo)
    return {
        "auth_token": res
    }

@app.post("/verifyToken", tags = ["Authentication"])
async def verifyToken(payload:dict) -> dict:
    token, username = payload["token"], payload["username"]
    try:
        decodedToken = jwtVerify(token)
    except Exception:
        return {
            "result": False
        }
    if not decodedToken:
        return {
            "result": False
        }
    elif decodedToken["username"] != username:
        return {
            "result": False
        }
    else:
        return {
            "result": True
        }

@app.post("/getMusic", tags=["Music"])
async def getMusic(userInfo:dict) -> dict:
    global db 
    username, hasPref = userInfo["username"], userInfo["hasPref"]
    if hasPref:
        res = await rec.nnMusic(db, username)
    else:
        res = await rec.randomSelect(db)
    ids = [item.track_id for item in res]
    thmb = spfy.queryById(ids)
    for idx, li in enumerate(thmb):
        res[idx].thumbnail = li
    return {
        "result": res
    }

@app.post("/getPlaylist", tags=["Music, Deprecated"])
async def getPlayList(payload:dict) -> dict:
    global db
    username = payload["username"]
    res = await dbq.getPlaylist(db, username)
    return {
        "result": res
    }

@app.post("/createPlaylist", tags=["Music, Deprecated"])
async def getPlayList(payload:dict) -> dict:
    global db
    username, playlist = payload["username"], payload["playlist"]
    res = await mm.createPlaylist(db, username, playlist)
    return {
        "result": res
    }

@app.post("/addToPlaylist", tags=["Music"])
async def getPlayList(payload:dict) -> dict:
    global db
    username, playlist_name, song_idx = payload["username"], payload["playlist_name"], payload["song_idx"]
    res = await mm.addToPlaylist(db, username, playlist_name, song_idx)
    return {
        "result": res
    }

@app.post("/deleteFromPlaylist", tags=["Music"])
async def getPlayList(payload:dict) -> dict:
    global db
    username, playlist_name, song_idx = payload["username"], payload["playlist_name"], payload["song_idx"]
    res = await mm.deleteFromPlaylist(db, username, playlist_name, song_idx)
    return {
        "result": res
    }

@app.post("/getPlaylistItems", tags=["Music"])
async def getPlaylistItems(payload:dict) -> dict:
    global db
    username, playlist_name = payload["username"], payload["playlist_name"]
    data = await dbq.getPlaylistItem(db, username, playlist_name)
    search = [element.song_id for element in data]
    res = await dbq.getMusicInfoBySongID(db, search)
    ids = [item.track_id for item in res]
    thmb = spfy.queryById(ids)
    for idx, li in enumerate(thmb):
        res[idx].thumbnail = li
    return {
        "result": res
    }

@app.post("/search", tags=["Search"])
async def searchItem(payload:dict) -> dict:
    global db
    category, query = payload["category"], payload["query"]
    res = await dbq.patternMatchSearch(db, category, query, 10)
    ids = [item.track_id for item in res]
    exists = await dbq.existInPlaylist(db, ids, "best_playlist")
    thmb = spfy.queryById(ids)
    for idx, li in enumerate(thmb):
        res[idx].thumbnail = li
        res[idx].existInPlaylist = exists[idx]["exists"]
    return {
        "result": res
    }