import asyncpg
import os
from dotenv import load_dotenv
import hashlib
from app.model import MusicWrap, UserWrap

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
                self.pool.close()
            except Exception as e:
                print("Error occured when trying to close pool")

    def getPool(self):
        return self.pool
    
    @staticmethod
    def encryptPassword(password):
        logf = open("error.log", "w")
        try:
            byte_string = password.encode('utf-8')
            sha256 = hashlib.sha256()
            sha256.update(byte_string)
            encrypt = sha256.hexdigest()
            return encrypt
        except Exception as e:
            logf.write(str(e))
            logf.close()
            return []
    
    @staticmethod
    async def userExists(db, **kwargs):
        logf = open("error.log", "w")
        try:
            context = "SELECT * FROM users WHERE username = $1;"
            output = await DBManager.query(db, context, kwargs['username'])
        except Exception as e:
            logf.write(str(e))
            logf.close()
            output = ['1']
        return len(output) > 0
    
    @staticmethod
    async def query(db, context, *args):
        async with db.getPool().acquire() as connection:
            row = await connection.fetch(context, *args)
            if row is not None:
                return [UserWrap(**item) for item in row]
        return []

