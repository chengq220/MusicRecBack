from app.model import MusicWrap, UserWrap, PlaylistWrap

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
    query = "SELECT * FROM user2playlist WHERE username = $1;"
    async with db.getPool().acquire() as connection:
        res = await connection.fetch(query, username)
        return [UserWrap(**item) for item in res]

async def getPlaylistItem(db, username, playlist):
    query = "SELECT * FROM playlist WHERE username = $1 AND playlist_name = $2;"
    async with db.getPool().acquire() as connection:
        res = await connection.fetch(query, username, playlist)
        return [PlaylistWrap(**item) for item in res]
    
async def getMusicInfoByID(db, song_idx):
    query = "SELECT DISTINCT ON (track_id) * FROM musicdata WHERE track_id = ANY($1) ORDER BY track_id, idx;"
    async with db.getPool().acquire() as connection:
        res = await connection.fetch(query, song_idx)
        return [MusicWrap(**item) for item in res]
    
async def nearestneighbor(db, vector, limit):
    query = "SELECT DISTINCT ON (track_id) * FROM musicdata ORDER BY track_id, feature <-> $1 LIMIT $2;"
    async with db.getPool().acquire() as connection:
        res = await connection.fetch(query, vector, limit)
        return [MusicWrap(**item) for item in res]
    
    