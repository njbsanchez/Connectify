import os
import json
from pprint import pprint

# from flask_oauth import OAuth
from spotipy import Spotify, CacheHandler

import crud
from model import SpotifyTokenInfo

SPOITFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")


class CacheDBHandler(CacheHandler):
    def __init__(self, session):
        self.session = session  # Flask session object

    def get_cached_token(self):
        """Get token user that's logged in."""
        
        if "user_id" not in self.session:
            return None
        
        user = crud.get_user_by_id(self.session["user_id"])
        
        return user.get_token_info()
    
    def save_token_to_cache(self, token_info):
        user = crud.get_user_by_id(self.session["user_id"])

        if not user.sp_token_info:
            user.sp_token_info = SpotifyTokenInfo()

        user.sp_token_info.access_token = token_info.get("access_token")
        user.sp_token_info.expires_in = token_info.get("expires_in")


class CacheSessionHandler(CacheHandler):
    def __init__(self, session, token_key):
        self.token_key = token_key
        self.session = session

    def get_cached_token(self):
        return self.session.get(self.token_key)

    def save_token_to_cache(self, token_info):
        self.session[self.token_key] = token_info
        self.session.modified = True
        

def get_sp_oauth(o_auth):
    print(f"Cached token: {o_auth.get_cached_token()}")
   
    if o_auth.validate_token(o_auth.get_cached_token()):
        sp_oauth = Spotify(auth_manager=o_auth)
        return sp_oauth
    

def update_spotify_info(oauth_manager):

    sp_oauth = get_sp_oauth(oauth_manager)
   
    results = sp_oauth.current_user()
   
    user_info = {
        "display_name": results['display_name'],
        "email": results['email'],
        "followers": results['followers']['total'],
        "s_id": results['id'],
        "images": results['images'][0]['url']
    }
    
    user = crud.get_user_by_id(session["user_id"])
    
    user.s_id = user_info["s_id"]
    user.recent_activity = user_info["recent_activity"]
    # user.sp_user_info = user_info["sp_user_info"]
    # user.display_name = user_info["display_name"]
    # user.email = user_info["email"]
    # user.followers = user_info["followers"]
    # user.images = user_info["images"]

    db.session.add(user)
    db.session.commit()
    
    return user_info

def get_playlists_from_sp(oauth_manager):
    """
    From Spotify, get name, id, and put into a list called "playlists".
    To be used for "edit my top playlist" page
    """
    sp_oauth = get_sp_oauth(oauth_manager)
    
    sp_playlists = sp_oauth.current_user_playlists(limit=3)
   
    playlists = []
    
    for playlist in sp_playlists['items']:
        playlist_entry = {'sp_playlist_id':playlist['id'],
                        'playlist_name':playlist['name'],
                       'playlist_desc':playlist['description'],
                       's_id':playlist['owner']['id'],
                       'play_url':playlist['external_urls']['spotify'],
                    #    'href':playlist['external_urls']['href']
                        }
        playlists.append(playlist_entry)
        
    with open('data/playlists.json','w') as outfile:
        json.dump(playlists, outfile)
    print("************ successfully pulled playlists from spotify and moved to json *******")
    
    return playlists

def update_my_playlists(user_id, oauth_manager):
    
    crud.clear_playlists()
    
    playlists = get_playlists_from_sp(oauth_manager)
    
    for playlist in playlists:
        crud.add_playlist(playlist["sp_playlist_id"], playlist["s_id"], playlist["playlist_name"], playlist["play_url"], playlist["playlist_desc"], user_id)
        
    print("************* successfully uploaded all playlists to current user ************")

def get_tracks_from_sp(oauth_manager):
    
    sp_oauth = get_sp_oauth(oauth_manager)

    sp_tracks = sp_oauth.current_user_top_tracks(time_range="long_term", limit=10)
    
    tracks = []
    
    for track in sp_tracks['items']:
        track_entry = {'sp_track_id':track['id'],
                       'track_name':track['name'],
                       'artist_name':track['artists'][0]['name'],
                       'artist_id':track['artists'][0]['id'],
                       'popularity':track['popularity'],
                    #    'genres':track['genres'],
                        }
        tracks.append(track_entry)
    
    with open('data/tracks.json','w') as outfile:
        json.dump(tracks, outfile)
    
    print("************ successfully pulled tracks from spotify and moved to json *******")
    
    return tracks

def update_my_tracks(user_id, oauth_manager):
    """to update tracks in user's database"""
    
    crud.clear_tracks()
    
    tracks = get_tracks_from_sp(oauth_manager)
    
    for track in tracks:
        crud.add_track(user_id, track["track_name"], track["sp_track_id"], track["artist_name"], track["artist_id"])
        
    print("************* successfully uploaded all playlists to current user ************")
                                                               
def get_artists_from_sp(oauth_manager):
    
    sp_oauth = get_sp_oauth(oauth_manager)
    
    sp_artists = sp_oauth.current_user_top_artists(time_range="long_term", limit=10)

    artists = []

    for artist in sp_artists['items']:
        artist_info = {'sp_artist_id':artist['id'],
                       'artist_name':artist['name'],
                    #    'genres':artist['genres'],
                       'popularity':artist['popularity'],
                       'images':artist['images']
                       }
        artists.append(artist_info)
    
    with open('data/artists.json','w') as outfile:
        json.dump(artists, outfile)
    
    print("************ successfully pulled artists from spotify and moved to json *******")

    return artists

def update_my_artists(user_id, oauth_manager):
    """to update tracks in user's database"""
    
    crud.clear_artists()
    
    artists = get_artists_from_sp(oauth_manager)
    
    for artist in artists:
        crud.add_artist(user_id, artist["sp_artist_id"], artist["artist_name"])
    
    print("************* successfully uploaded all artists to current user ************")
                            
