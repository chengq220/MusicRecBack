from app.model import MusicWrap

async def getTableSize(db, table):
    context = f'SELECT COUNT(*) FROM "{table}";'
    async with db.getPool().acquire() as connection:
        size = await connection.fetchval(context)
        return size

async def getMusicBetweenIndices(db, lb, ub):
    context = "SELECT * FROM musicdata WHERE idx BETWEEN $1 AND $2;"
    async with db.getPool().acquire() as connection:
        res = await connection.fetch(context, lb, ub)
        return [MusicWrap(**item) for item in res]