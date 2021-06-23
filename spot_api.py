import os
import crud
from flask import (
    Flask,
    render_template,
    session,
    request,
    redirect,
    url_for,
    flash,
)
import server
import json
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
    redirect_uri="http://localhost:5000/home",
    scope="user-read-email playlist-read-private playlist-read-collaborative user-top-read",
    cache_handler=CacheSessionHandler(session, "spotify_token"))

def get_sp_oauth(o_auth):
    
    if not o_auth.validate_token(o_auth.get_cached_token()):
        flash("Please authenticate your Spotify profile in order to proceed.")
        return redirect("/")
    else:
        sp_oauth = Spotify(auth_manager=oauth_manager)
        return sp_oauth

def get_spotify_info():

    sp_oauth = get_sp_oauth(oauth_manager)
   
    results = sp_oauth.current_user()
   
    display_name, email, followers, s_id, images = (
                    results['display_name'],
                    results['email'],
                    results['followers']['total'],
                    results['id'],
                    results['images'][0]['url'],
                    )
    
    user = crud.get_user_by_id(session["user_id"])
    
    user = User(s_id=s_id, recent_activity=recent_activity)

    db.session.add(user)
    db.session.commit()
    
    return sp_user_info, display_name, email, followers, s_id, images
   
def get_my_playlists():
    """
    From Spotify, get name, id, and put into a list called "playlists".
    To be used for "edit my top playlist" page
    """
    sp_oauth = get_sp_oauth(oauth_manager)
    
    sp_playlists = sp_oauth.current_user_playlists(limit=5)
   
    playlists = []
    
    for playlist in sp_playlists['items']:
        playlist_entry = {'sp_playlist_id':playlist['id'],
                        'playlist_name':playlist['name'],
                       'playlist_desc':playlist['description'],
                       'owner_id':playlist['owner']['id'],
                       'play_url':playlist['external_urls']['spotify'],
                    #    'href':playlist['external_urls']['href']
                        }
        playlists.append(playlist_entry)
        
    # with open('data/playlists.json','w') as outfile:
    #     json.dump(playlists, outfile)
    # print("************ successfully uploaded playlists to json *******")
    
    return playlists
    
    #----create a view function----#

def update_track_db():
    """to update tracks in user's database"""
    
    tracks_in_db = []
    tracks = get_my_playlists()
    user_id = session['user_id']
    
    for track in tracks:
        sp_track_id, track_name, artist, artist_id, popularity, genres = (
            track["sp_track_id"],
            track["track_name"],
            track["artist"],
            track["artist_id"],
            track["popularity"],
            # track["genre"],
        )
        
        db_track = crud.add_track(sp_track_id, track_name, artist, artist_id, popularity, genres, user_id)
        tracks_in_db.append(db_track)
                                           

def get_all_tracks():
    
    sp_oauth = get_sp_oauth(oauth_manager)
     
    tracks = []

    results = sp_oauth.current_user_top_tracks(time_range="long_term", limit=200)
    for track in results['items']:
        track_entry = {'sp_track_id':track['id'],
                       'track_name':track['name'],
                       'artist_id':track['artists'][0]['id'],
                       'popularity':track['popularity'],
                    #    'genres':track['genres'],
                        }
        tracks.append(track_entry)
    
    # with open('data/tracks.json','w') as outfile:
    #     json.dump(tracks, outfile)
    # print("************ successfully uploaded tracks to json *******")
    
    return tracks

def update_track_db():
    """to update tracks in user's database"""
    
    tracks_in_db = []
    tracks = get_my_playlists()
    user_id = session['user_id']
    
    for track in tracks:
        sp_track_id, track_name, artist_name, artist_id = (
            track["sp_track_id"],
            track["track_name"],
            track["artist"],
            track["artist_id"]
            # track["popularity"],
            # track["genre"],
        )
        
        db_track = crud.add_track(sp_track_id, track_name, artist, artist_id, popularity, genres, user_id)
        tracks_in_db.append(db_track)
    
    
# def get_my_artists():
#     """Load user's real top_artists into database."""
        
#     sp_oauth = get_sp_oauth(oauth_manager)
    
#     user_id = session.get('user_id')

#     results = sp_oauth.current_user_top_artists(time_range="long_term", limit=10, offset=10)
    
#     for artist in results['items']:
#         sp_artist_id, artist_name = (artist['id'],
#                                      artist['name'],
#                                     #  artist['genres'],
#                                     #  artist['popularity'],
#                                     #  artist['images']
#         )
    
#     session.query(artist).filter(artist.user_id==user_id).delete()
    
#     db_artists = crud.add_artist(user_id, sp_artist_id, artist_name)
#     dum_artists_in_db.append(db_artists)
#     model.db.session.commit()
    

                                                                   
def get_my_artists():
    
    sp_oauth = get_sp_oauth(oauth_manager)
    
    artists = []

    results = sp_oauth.current_user_top_artists(time_range="long_term", limit=10, offset=10)
    for artist in results['items']:
        artist_info = {'sp_artist_id':artist['id'],
                       'artist_name':artist['name'],
                    #    'genres':artist['genres'],
                       'popularity':artist['popularity'],
                       'images':artist['images']
                       }
        artists.append(artist_info)
    
    with open('data/artists.json','w') as outfile:
        json.dump(artists, outfile)
    print("************ successfully uploaded artists to json *******")

    return artists

def update_artist_db():
    """to update tracks in user's database"""
    
    artists_in_db = []
    artists = get_my_artists()
    user_id = session['user_id']
    
    for artist in artists:
        sp_artist_id, artist_name, genre, popularity, image = (
            artist["sp_artist_id"],
            artist["artist_name"],
            # artist["genre"],
            artist["popularity"],
            artist["image"],
        )
        db_artist = crud.add_artist(sp_artist_id, artist_name, genre, popularity, image, user_id)
        artists_in_db.append(db_artist)
        
