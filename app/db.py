import asyncpg
import os
from dotenv import load_dotenv

class database():
    def __init__(self):
        self.pool = None
    
    async def connect(self):
        load_dotenv()
        dbname = os.getenv("POSTGRES_DB")
        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        dburl = os.getenv("DATABASE_URL")

        self.pool = await asyncpg.create_pool(
            user=user,
            password=password,
            database=dbname,
            host=dburl,
            port=5432
        )
    
    async def disconnect(self):
        self.pool.close()

    async def query(self, context):
        async with database.pool.acquire() as connection:
            row = await connection.fetchrow(context)
            if row is not None:
                return row
        return None