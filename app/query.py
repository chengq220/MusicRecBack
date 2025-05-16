from app.model import MusicWrap
# Fucntions to access the db
async def execContext(db, context):
    async with db.getPool().acquire() as connection:
        row = await connection.fetchrow(context)
        if row is not None:
            print(dict(row))
            return MusicWrap(**row)
    return None