from app.model import MusicWrap, UserWrap

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
    

async def getPref(db, user):
    context = "SELECT * FROM users WHERE username = $1;"
    async with db.getPool().acquire() as connection:
        res = await connection.fetch(context, user)
        return [UserWrap(**item) for item in res]
    
async def getPlaylist(db, username):
    query = "SELECT * FROM playlist WHERE username = $1;"
    async with db.getPool().acquire() as connection:
        res = await connection.fetch(query, username)
        return res
    
    