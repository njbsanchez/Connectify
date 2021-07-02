import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

user = 'spotify'

if len(sys.argv) > 1:
    user = sys.argv[1]

playlists = sp.user_playlists(user)

while playlists:
    for playlist in playlists['items']:
        
    spot_id, playlist_description, uri, name = (
        playlist['id'],
        playlist['description'],
        playlist['uri'],
        playlist['name']
    ) 
             
    if playlist['next']:
        playlists = sp.next(playlist)
    else:
        playlists = None