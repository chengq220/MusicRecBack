from app.model import MusicWrap
# Fucntions to access the db
async def execContext(db, context):
    async with db.getPool().acquire() as connection:
        row = await connection.fetch(context)
        if row is not None:
            return [MusicWrap(**item) for item in row]
    return None