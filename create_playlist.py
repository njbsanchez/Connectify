import json

import requests
import random

from model import Track, Playlist, User
import crud
from flask import session


class SpotifyClient:
    """SpotifyClient performs operations using the Spotify API."""

    def __init__(self, authorization_token, user_id):
        self._authorization_token = authorization_token
        self._user_id = user_id

    def create_playlist(self, playlist_name):
        
        user_id= session['user_id']
        user = crud.get_user_by_id(user_id)
        data = json.dumps({
            "name": f"{playlist_name}",
            "description": f"Playlist curated from a few favorites.",
            "public": True
        })
        url = f"https://api.spotify.com/v1/users/{self._user_id}/playlists"
        response = self.post_api_request(url, data)
        response_json = response.json()
        # create playlist
        play_desc = data[1]
        s_id = response_json["owner"].get("id")
        sp_playlist_id = response_json["id"]
        play_url = response_json["external_urls"].get("spotify")
        playlist = crud.create_playlist(sp_playlist_id, s_id, playlist_name, user_id, play_url, play_desc)

        return playlist

    def populate_playlist(self, playlist, tracks):
        """Add tracks to a playlist."""
        track_uris = [track.create_spotify_uri() for track in tracks]
        data = json.dumps(track_uris)
        print(data, "***************************")
        url = f"https://api.spotify.com/v1/playlists/{playlist.sp_playlist_id}/tracks"
        response = self.post_api_request(url, data)
        response_json = response.json()

        return response_json

    def get_api_request(self, url):
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._authorization_token}"
            }
        )
        return response

    def post_api_request(self, url, data):
        response = requests.post(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._authorization_token}"
            }
        )
        return response