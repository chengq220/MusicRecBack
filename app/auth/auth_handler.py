from dotenv import load_dotenv
import os
import time
import jwt
from fastapi import HTTPException

load_dotenv()

def signJWT(user:dict) -> str:
    payload = {
        "username": user["username"],
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, os.getenv("SECRET"), algorithm=os.getenv("ALGORITHM"))
    return token

def decodeJWT(token :str) -> dict:
    try:
        decoded_token = jwt.decode(token, os.getenv("SECRET"), algorithms=[os.getenv("ALGORITHM")])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception as e:
        return {}
    
def jwtVerify(token:str) -> dict:
    decoded = decodeJWT(token)
    if not decoded:
        raise HTTPException(status_code=401, detail="Token not correct")
    return decoded

