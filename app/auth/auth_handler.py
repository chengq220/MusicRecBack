from dotenv import load_dotenv
import os
import time
import jwt

load_dotenv()

def signJWT(user) -> dict[str, str]:
    payload = {
        "username": user.username,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, os.getenv("SECRET"), algorithm=os.getenv("ALGORITHM"))
    return {
        "access_token": token
    }

def decodeJWT(token :str) -> dict:
    try:
        decoded_token = jwt.decode(token, os.getenv("SECRET"), algorithm=os.getenv("ALGORITHM"))
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}