import logging

# Set up logging
# logging.basicConfig(
#     filename='app.log',      # Log file name
#     level=logging.ERROR,     # Only log errors and above
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

async def registerUser(db, username, password):
    query = "INSERT INTO users (username, password, new_user) VALUES ($1, $2, TRUE);"
    async with db.getPool().acquire() as connection:
        res = await connection.execute(query, username, password)
        return res

async def updateUserPreference(db, user, artist, genre):
    query = "UPDATE users SET fav_genre = $1, fav_artist = $2, new_user = FALSE WHERE username = $3;"
    async with db.getPool().acquire() as connection:
        res = await connection.execute(query, genre, artist, user)
        return res
    
async def createPlaylist(db, username, playlist="default1"): #only create playlist when there is song being added
    query = "SELECT * FROM playlist WHERE username = $1 AND playlist_name = $2;"
    async with db.getPool().acquire() as connection:
        res = await connection.fetch(query, username, playlist)
        return res
    