import os
from flask import (
    Flask,
    render_template,
    session,
    request,
    redirect,
    url_for,
    flash,
)

# from flask_oauth import OAuth
from spotipy import Spotify, CacheHandler
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from pprint import pprint

SPOITFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

class CacheSessionHandler(CacheHandler):
    def __init__(self, session, token_key):
        self.token_key = token_key
        self.session = session

    def get_cached_token(self):
        return self.session.get(self.token_key)

    def save_token_to_cache(self, token_info):
        self.session[self.token_key] = token_info
        session.modified = True

oauth_manager = SpotifyOAuth(
    client_id=SPOITFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri="http://localhost:5000",
    scope="user-read-email playlist-read-private playlist-read-collaborative user-top-read",
    cache_handler=CacheSessionHandler(session, "spotify_token"))

def get_sp_oauth(o_auth):
    
    if not o_auth.validate_token(o_auth.get_cached_token()):
        return redirect("/")
    else:
        sp_oauth = Spotify(auth_manager=oauth_manager)
        return sp_oauth

def get_spotify_info():
    if not oauth_manager.validate_token(oauth_manager.get_cached_token()):
        return redirect("/")

    sp = Spotify(auth_manager=oauth_manager)

    return render_template("spotify-info.html", spotify=sp)

def get_my_playlists():
    """
    From Spotify, get name, id, and put into a list called "playlists".
    To be used for "edit my top playlist" page
    """
   
    if not oauth_manager.validate_token(oauth_manager.get_cached_token()):
            return redirect("/")
    else:
        sp_oauth = Spotify(auth_manager=oauth_manager)
    
    sp_playlists = sp_oauth.current_user_playlists(limit=4)
    
    playlists = []
    
    for i, item in enumerate(sp_playlists['items']):                                          
        print("%d ---- %s %s %s" % (i, item['name'], item['id'], item['tracks']))
        playlists.append( {(i, item['name']): [item['id'],item['tracks']]})  
    
    return playlists
    
    #----create a view function----#
    
def get_all_tracks():
    
    sp_oauth = get_sp_oauth(oauth_manager)
    
    short_term = []
    medium_term = []
    long_term = []

    ranges = [short_term, medium_term,long_term]
    
    for sp_range in ranges:
        results = sp_oauth.current_user_top_tracks(time_range=sp_range, limit=50)
        for track in results['items']:
            track_entry = {track['id']: 
                                    {
                                    'track_name':track['name'],
                                    'artist':track['artists'][0]['name'],
                                    'artist_id':track['artists'][0]['id'],
                                    'popularity':track['popularity'],
                                    # 'album':track['album'][0]['name'],
                                    # 'genres':track['genres']
                                    }
                          }
            sp_range.append(track_entry)
                
    # for range in ranges:
    #     print("")
    #     print("")
    #     print("********** Next Section *************")
    #     print("")
    #     for track in range:
    #         print(track)
    #         print(track['name'], '//', track['artists'][0]['name'], '//',  track['artists'][0]['uri'])

    return ranges

def get_all_artists():
    
    sp_oauth = get_sp_oauth(oauth_manager)
    
    short_term = []
    medium_term = []
    long_term = []

    ranges = [short_term, medium_term,long_term]
    
    for sp_range in ranges:
        results = sp_oauth.current_user_top_artists(time_range=sp_range, limit=50)
        for artist in results['items']:
            artist_info = {artist['id']: 
                                    {
                                    'artist':artist['name'],
                                    'genres':artist['genres'],
                                    'popularity':artist['popularity'],
                                    'images':artist['images']
                                    }
                          }
            sp_range.append(artist_info)
   
    for range in ranges:
        print("")
        print("")
        print("********** Next Section *************")
        print("")
    for artist in range:
        print(artist)

    return ranges

