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
import spotipy
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

app = Flask(__name__)
app.secret_key = "DEV"
oauth_manager = SpotifyOAuth(
    client_id=SPOITFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri="http://localhost:5000",
    scope="user-read-email playlist-read-private playlist-read-collaborative user-top-read",
    cache_handler=CacheSessionHandler(session, "spotify_token"),
)

@app.route("/")         #move to main server doc
def homepage():
    jinja_env = {}

    if request.args.get("code") or oauth_manager.validate_token(
        oauth_manager.get_cached_token()    
    ):
        oauth_manager.get_access_token(request.args.get("code"))
        return redirect("/spotify-info")

    return render_template(
        "index.html", spotify_auth_url=oauth_manager.get_authorize_url()
    )


def get_spotify_info():
    if not oauth_manager.validate_token(oauth_manager.get_cached_token()):
        return redirect("/")

    sp = Spotify(auth_manager=oauth_manager)

    return render_template("spotify-info.html", spotify=sp)


@app.route("/playlist")
def get_my_playlists():
    """
    From Spotify, get name, id, and put into a list called "playlists".
    """
   
    if not oauth_manager.validate_token(oauth_manager.get_cached_token()):
            return redirect("/")
    else:
        sp_oauth = Spotify(auth_manager=oauth_manager)
    
    sp_playlists = sp_oauth.current_user_playlists(limit=50)
    
    playlists = []
    
    for i, item in enumerate(sp_playlists['items']):                                          
        print("%d ---- %s %s %s" % (i, item['name'], item['id'], item['tracks']))
        playlists.append( {(i, item['name']): [item['id'],item['tracks']]})  
    
    print(playlists)
    
    #----create a view function----#
    
    return render_template("play.html", spotify=sp_oauth, playlists=playlists)

@app.route("/tracks")
def get_tracks():
    if not oauth_manager.validate_token(oauth_manager.get_cached_token()):
            return redirect("/")

    sp = Spotify(auth_manager=oauth_manager)
    
    short_term = []
    medium_term = []
    long_term = []

    ranges = [short_term, medium_term,long_term]
    
    for sp_range in ranges:
        results = sp.current_user_top_tracks(time_range=sp_range, limit=50)
        for track in results['items']:
            track_info = {track['id']: 
                                    {
                                    'track_name':track['name'],
                                    'artist':track['artists'][0]['name'],
                                    'artist_id':track['artists'][0]['id'],
                                    'popularity':track['popularity'],
                                    'album':track['album'][0]['name'],
                                    'genres':track['genres']
                                    }
                          }
            sp_range.append(track_info)
                
    for range in ranges:
        print("")
        print("")
        print("********** Next Section *************")
        print("")
        for track in range:
            print(track)
            # print(track['name'], '//', track['artists'][0]['name'], '//',  track['artists'][0]['uri'])

    return render_template("tracks.html", short_term=short_term)

@app.route("/artists")
def get_artists():
    if not oauth_manager.validate_token(oauth_manager.get_cached_token()):
            return redirect("/")

    sp = Spotify(auth_manager=oauth_manager)
    
    short_term = []
    medium_term = []
    long_term = []

    ranges = [short_term, medium_term,long_term]
    
    for sp_range in ranges:
        results = sp.current_user_top_artists(time_range=sp_range, limit=50)
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
            # print(track['name'], '//', track['artists'][0]['name'], '//',  track['artists'][0]['uri'])

    return render_template("artist.html", short_term=short_term)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, use_debugger=True)
