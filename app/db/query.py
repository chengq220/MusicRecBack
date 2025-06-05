from app.model import MusicWrap, UserWrap, PlaylistWrap

async def getTableSize(db, table):
    context = f'SELECT COUNT(*) FROM "{table}";'
    async with db.getPool().acquire() as connection:
        size = await connection.fetchval(context)
        return size

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
    
async def getMusicBetweenIndices(db, lb, ub):
    context = "SELECT * FROM musicdata WHERE id BETWEEN $1 AND $2;"
    async with db.getPool().acquire() as connection:
        res = await connection.fetch(context, lb, ub)
        return [MusicWrap(**item) for item in res]
    
async def getMusicInfoBySongID(db, song_idx):
    query = """SELECT DISTINCT ON (track_id) * FROM musicdata 
                WHERE track_id = ANY($1) ORDER BY track_id, id;"""
    async with db.getPool().acquire() as connection:
        res = await connection.fetch(query, song_idx)
        return [MusicWrap(**item) for item in res]
    
async def getMusicInfoByID(db, id):
    query = """SELECT DISTINCT ON (track_id) * FROM musicdata 
                WHERE id = ANY($1) ORDER BY track_id, id;"""
    async with db.getPool().acquire() as connection:
        res = await connection.fetch(query, id)
        return [MusicWrap(**item) for item in res]
    
async def nearestneighbor(db, vector, limit):
    query = """SELECT DISTINCT ON (track_id) * FROM musicdata 
                WHERE track_id NOT IN (SELECT song_id FROM playlist) 
                ORDER BY track_id, feature <-> $1 LIMIT $2;"""
    async with db.getPool().acquire() as connection:
        res = await connection.fetch(query, vector, limit)
        return [MusicWrap(**item) for item in res]
    
async def getAvgPreference(db, username):
    query = """SELECT AVG(feature) FROM musicdata 
                INNER JOIN playlist ON musicdata.track_id = playlist.song_id 
                WHERE playlist.username = $1;"""
    async with db.getPool().acquire() as connection:
        vec = await connection.fetchval(query, username)
        return vec

async def patternMatchSearch(db, category, item, limit):
    if(category == "Artist"):
        query = """SELECT DISTINCT ON (track_id) * 
                    FROM musicdata WHERE artists ~* $1 
                    ORDER BY track_id LIMIT $2;"""
    elif(category == "Genre"):
        query = """SELECT DISTINCT ON (track_id) * 
                    FROM musicdata WHERE genre ~* $1 
                    ORDER BY track_id LIMIT $2;"""
    else:
        query = """SELECT DISTINCT ON (track_id) * 
                    FROM musicdata WHERE track_name ~* $1 
                    ORDER BY track_id LIMIT $2;"""
    async with db.getPool().acquire() as connection:
        res = await connection.fetch(query, item, limit)
        return [MusicWrap(**item) for item in res]
    

async def existInPlaylist(db, ids, playlist_name):
    query = """WITH input_idx AS (SELECT UNNEST($1::text[]) AS idx) 
                SELECT playlist.song_id IS NOT NULL AS exists
                FROM input_idx LEFT JOIN playlist ON playlist.song_id = input_idx.idx AND playlist.playlist_name = $2"""
    async with db.getPool().acquire() as connection:
        res = await connection.fetch(query, ids, playlist_name)
        return res
    
    

    
    