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
    
async def getPlaylistNames(db, username):
    query = "SELECT * FROM user2playlist WHERE username = $1;"
    async with db.getPool().acquire() as connection:
        res = await connection.fetch(query, username)
        return [UserWrap(**item) for item in res]

async def getPlaylistItem(db, username, playlist=None):
    async with db.getPool().acquire() as connection:
        if(playlist):
            query = "SELECT * FROM playlist WHERE username = $1 AND playlist_name = $2;"
            res = await connection.fetch(query, username, playlist)
        else:
            query = "SELECT * FROM playlist WHERE username = $1;"
            res = await connection.fetch(query, username)
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
                    FROM musicdata WHERE track_genre ~* $1 
                    ORDER BY track_id LIMIT $2;"""
    else:
        query = """SELECT DISTINCT ON (track_id) * 
                    FROM musicdata WHERE track_name ~* $1 
                    ORDER BY track_id LIMIT $2;"""
    async with db.getPool().acquire() as connection:
        res = await connection.fetch(query, item, limit)
        return [MusicWrap(**item) for item in res]
    

async def existInPlaylist(db, ids, playlist_name):
    query = """ WITH 
                input_idx AS (SELECT UNNEST($1::text[]) AS song_id),
                playlist_idx AS (SELECT UNNEST($2::text[]) AS playlist_name),
                cross_pairs AS (
                    SELECT song_id, playlist_name FROM input_idx CROSS JOIN playlist_idx
                ),
                exist_pair AS (SELECT 
                cross_pairs.song_id,
                cross_pairs.playlist_name,
                (playlist.song_id IS NOT NULL) AS exists
                FROM cross_pairs
                LEFT JOIN playlist
                ON playlist.song_id = cross_pairs.song_id AND playlist.playlist_name = cross_pairs.playlist_name)
                SELECT * from exist_pair where exists = true;
                """
    async with db.getPool().acquire() as connection:
        res = await connection.fetch(query, ids, playlist_name)
        return [dict(item) for item in res]
    
    

    
    