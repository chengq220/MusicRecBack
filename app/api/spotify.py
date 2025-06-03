import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

class Spotify():
    def __init__(self):
        self.sp = self.__initSpotify()
    
    def __initSpotify(self):
        load_dotenv()
        client_id = os.getenv("SPOTIFY_ID")
        client_secret = os.getenv("SPOTIFY_SECRET")
        mnger = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        return spotipy.Spotify(auth_manager=mnger)
            
    def queryById(self, ids: list) -> list:
        if(len(ids) == 1):
            result = [self.sp.track(ids[0])]
        else:
            result = self.sp.tracks(ids)['tracks']
        images = []
        for item in result:
            img_url = item["album"]["images"][0]["url"]
            images.append(img_url)
        return images
        
    

