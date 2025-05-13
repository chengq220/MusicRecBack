from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3000/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

backPref = None


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome safas dfasf ."}

@app.get("/todo", tags=["todos"])
async def get_todos() -> dict:
    return { "data": 1 }

@app.post("/pref", tags=["preference"])
async def set_pref(pref: str) -> dict:
    global backPref 
    backPref= pref
    return {
        "data": f"Successfully received: {pref}"
    }
