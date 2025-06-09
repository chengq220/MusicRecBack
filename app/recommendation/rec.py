import app.db.query as dbq
import random

NUM_DESIRE = 12

async def randomSelect(db):    
    size = await dbq.getTableSize(db, "musicdata")
    samples = random.sample(range(1, size), NUM_DESIRE)
    res = await dbq.getMusicInfoByID(db, samples)
    return res

async def nnMusic(db, username):
    vec = await dbq.getAvgPreference(db, username)
    res = await dbq.nearestneighbor(db, vec, NUM_DESIRE)
    return res