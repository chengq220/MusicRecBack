def insertThumbnail(spfy, res):
    ids = [item.track_id for item in res]
    thmb = spfy.queryById(ids)
    for idx, li in enumerate(thmb):
        res[idx].thumbnail = li
    return res