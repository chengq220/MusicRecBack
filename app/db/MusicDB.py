import asyncpg
import os
from dotenv import load_dotenv

class MusicDBManager():
    def __init__(self):
        self.pool = None
    
    async def connect(self):
        load_dotenv()
        dburl = os.getenv("MUSICDB_URL")
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