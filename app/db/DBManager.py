import asyncpg
import os
from dotenv import load_dotenv
import hashlib
from app.model import UserWrap

class DBManager():
    def __init__(self):
        self.pool = None
    
    async def connect(self):
        load_dotenv()
        dburl = os.getenv("DB_URL")
        try:
            self.pool = await asyncpg.create_pool(
                dsn=dburl, min_size=1, max_size=10
            )
        except Exception as e:
            print("Error occured when trying to initialized a connection to database") 

    
    async def disconnect(self):
        if self.pool is not None:
            try:
                await self.pool.close()
            except Exception as e:
                print("Error occured when trying to close pool")

    def getPool(self):
        return self.pool
    
    @staticmethod
    def encryptPassword(password):
        byte_string = password.encode('utf-8')
        sha256 = hashlib.sha256()
        sha256.update(byte_string)
        encrypt = sha256.hexdigest()
        return encrypt

    @staticmethod
    async def getUser(db, username):
        context = "SELECT * FROM users WHERE username = $1;"
        async with db.getPool().acquire() as connection:
            row = await connection.fetch(context, username)
            if row: 
                return [UserWrap(**item) for item in row]
        return []

