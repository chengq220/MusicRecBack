async def registerUser(db, username, password):
    query = "INSERT INTO users (username, password) VALUES ($1, $2);"
    async with db.getPool().acquire() as connection:
        res = await connection.execute(query, username, password)
        return res
    