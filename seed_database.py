"""Script to seed database."""

import os
import json
from datetime import datetime

import crud
import model
import server
import spot_api as sp


def get_dummies():
    """Load dummy users from dataset into database."""

    # Load dummy user data from JSON file
    with open("data/profile_OU.json") as f:
        dummy_users = json.loads(f.read())

    # Create dummy users, store them in list so we can use them
    dummies_in_db = []
    for user in dummy_users:
        email, password, name, s_id, latitude, longitude, recent_activity = (
            user["email"],
            user["password"],
            user["name"],
            user["s_id"],
            user["latitude"],
            user["longitude"],
            user["played_at"]
        )
        last_played = datetime.strptime(user["played_at"], "%Y-%m-%dT%H:%M:%S.%f%z")

        db_user = crud.create_user(email, password, name, s_id, latitude, longitude, recent_activity)
        dummies_in_db.append(db_user)

    model.db.session.commit()

def get_dum_tracks():
    """Load bears from dataset into database."""

    # Load dummy user data from JSON file
    with open("data/tracks_OU.json") as f:
        dummyuser_tracks = json.loads(f.read())

    # Create dummy users, store them in list so we can use them
    dum_tracks_in_db = []
    
    for user in dummyuser_tracks:
        for user_id, detail_array in user.items():
            user_id = int(user_id)
            for item in detail_array:
                 sp_track_id, track_name, artist_name, artist_id = (
                    item["sp_track_id"],
                    item["track_name"],
                    item["artist_name"],
                    item["artist_id"]
                 )
                 db_track = crud.add_track(user_id, track_name, sp_track_id, artist_name, artist_id)
                 dum_tracks_in_db.append(db_track)
                 model.db.session.commit()
    
    return dum_tracks_in_db

def get_dum_artists():
    """Load bears from dataset into database."""

    # Load dummy user data from JSON file
    with open("data/artists_OU.json") as f:
        dummyuser_artists = json.loads(f.read())

    # Create dummy users, store them in list so we can use them
    dum_artists_in_db = []
    for user in dummyuser_artists:
        for user_id, detail_array in user.items():
            user_id = int(user_id)
            for item in detail_array:
                sp_artist_id, artist_name = (
                    item["sp_artist_id"],
                    item["artist_name"]
                )
                db_artists = crud.add_artist(user_id, sp_artist_id, artist_name)
                dum_artists_in_db.append(db_artists)
                model.db.session.commit()
    
    return dum_artists_in_db

def get_dum_playlists():
    """Load bears from dataset into database."""

    # Load dummy user data from JSON file
    with open("data/playlists.json") as f:
        dummy_playlists = json.loads(f.read())

    # Create dummy users, store them in list so we can use them
    dum_playlists_in_db = []
    for item in dummy_playlists:
        for user_id, playlist_list in item.items():
            user_id = int(user_id)
            for playlist in playlist_list:
                sp_playlist_id, sp_user_id, playlist_name, play_url, play_desc= ( 
                    playlist["sp_playlist_id"], 
                    playlist["owner_id"], 
                    playlist["playlist_name"],
                    playlist["play_url"],
                    playlist["playlist_desc"]
                )

            db_playlist = crud.add_playlist(sp_playlist_id, sp_user_id, playlist_name, play_url, play_desc, user_id)
            dum_playlists_in_db.append(db_playlist)

    model.db.session.commit()

if __name__ == '__main__':

    os.system("dropdb trackify")
    os.system("createdb trackify")
    
    model.connect_to_db(server.app)
    model.db.create_all()

    print("************************ CHECK IF TRACKIFY DB CREATED ********************")
    
    get_dummies()
    
    print("************************ DUMMY USERS ADDED TO DB ********************")

    get_dum_artists()
    
    print("************************ DUMMY ARTISTS ADDED TO DB ********************")

    get_dum_tracks()
    
    print("************************ DUMMY ARTISTS ADDED TO DB ********************")


    model.db.session.commit()

