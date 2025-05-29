import logging

# Set up logging
# logging.basicConfig(
#     filename='app.log',      # Log file name
#     level=logging.ERROR,     # Only log errors and above
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

async def registerUser(db, username, password):
    query = "INSERT INTO users (username, password) VALUES ($1, $2);"
    async with db.getPool().acquire() as connection:
        res = await connection.execute(query, username, password)
        return res

async def updateUserPreference(db, user, artist, genre):
    query = "UPDATE users SET fav_genre = $1, fav_artist = $2, new_user = FALSE WHERE username = $3;"
    async with db.getPool().acquire() as connection:
        res = await connection.execute(query, genre, artist, user)
        return res
    
async def createPlaylist(db, user, playlist_name = "default1"):
    query = "INSERT INTO user2playlist (username, playlist) VALUES ($1, $2);"
    async with db.getPool().acquire() as connection:
        res = await connection.execute(query, user, playlist_name)
        return res
    
async def addToPlaylist(db, user, playlist_name, song_idx):
    query = "INSERT INTO playlist (username, playlist_name, song_id) VALUES ($1, $2, $3);"
    async with db.getPool().acquire() as connection:
        res = await connection.execute(query, user, playlist_name, song_idx)
        return res
    