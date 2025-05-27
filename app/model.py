from pydantic import BaseModel
from typing import Optional

class MusicWrap(BaseModel):
    idx: int
    track_id: str
    artists: str
    album_name: str
    track_name: str
    popularity: int
    duration_ms: int
    explicit: bool
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int 
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    time_signature: int
    track_genre: str


class UserWrap(BaseModel):
    id: Optional[int] = None
    username: str
    password: Optional[str] = None
    fav_genre: Optional[str] = None
    fav_artist: Optional[str] = None
    new_user: Optional[bool] = None
    playlist: Optional[str] = None


class PlaylistWrap(BaseModel):
    playlist_id: int
    username: str
    playlist_name: str
    song_id: int
    like: Optional[bool] = None
