from pydantic import BaseModel
from typing import Optional

# Wrapper for Music Data
class MusicWrap(BaseModel):
    id: int
    track_id: str
    artists: str
    album_name: str
    track_name: str
    track_genre: str
    feature: str
    thumbnail: Optional[str] = None
    existInPlaylist: Optional[bool] = None

# Wrapper for user profile
class UserWrap(BaseModel):
    id: Optional[int] = None
    username: str
    password: Optional[str] = None
    fav_genre: Optional[str] = None
    fav_artist: Optional[str] = None
    playlist: Optional[str] = None

# Map from user to playlist
class PlaylistWrap(BaseModel):
    username: str
    playlist_name: str
    song_id: str
    favorite: Optional[bool] = None
