"""CRUD operations."""
from model import db, User, connect_to_db, Playlist, Track, Artist
from flask import session

def create_user(email, password, name, s_id, latitude=None, longitude=None, recent_activity=None):
    """Create and return a new user."""

    user = User(email=email, password=password, name=name, s_id=s_id, latitude=latitude, longitude=longitude, recent_activity=recent_activity)

    db.session.add(user)
    db.session.commit()

    return user

def update_user_location(user, latitude, longitude):
    """Update user's latitude and longitude."""

    user.latitude = latitude
    user.longitude = longitude

    db.session.add(user)
    db.session.commit()

    return user


def get_user_by_id(id):
    """Return a user by id."""

    return User.query.filter(User.user_id == id).first()

def get_user_by_email(email):
    """Return a user by email."""
    
    return User.query.filter(User.email == email).first()

def get_user_by_spot(s_id):
    """Return a user by email."""

    return User.query.filter(User.s_id == s_id).first()

def get_users():
    """Return all users."""

    return User.query.all()

def add_playlist(sp_playlist_id, sp_id, playlist_name, play_url, play_desc, user_id):
    """Create and add playlist to DB."""

    playlist = Playlist(
        sp_playlist_id=sp_playlist_id, 
        s_id=s_id, 
        playlist_name=playlist_name, 
        user_id=user_id, 
        play_url=play_url, 
        play_desc=play_desc)

    db.session.add(playlist)
    db.session.commit()

    return playlist

def add_playlist_jsonformat (user_id, playlist):
    
    playlist_id, sp_playlist_id, sp_user_id, playlist_name = (
        playlist["playlist_id"], 
        playlist["sp_playlist_id"], 
        playlist["sp_user_id"], 
        playlist["playlist_name"], 
    )
    
    playlist = Playlist(
        playlist_id=playlist_id,
        sp_playlist_id=sp_playlist_id,
        sp_user_id=sp_user_id, 
        playlist_name=playlist_name,
        user_id=user_id
    )
    
    db.session.add(playlist)
    db.session.commit()
    
    return playlist

def add_track(user_id, track_name, sp_track_id, artist_name, artist_id):
    
    track = Track(
        track_name=track_name,
        sp_track_id=sp_track_id,
        artist_name=artist_name,
        artist_id=artist_id, 
        user_id=user_id
    )
    
    db.session.add(track)
    db.session.commit()
    
    return track

# def update_user_artists():
#     """Load bears from dataset into database."""

#     session.query(artist).filter(artist.user_id==session["user_id"]).delete()
    
#     # Load dummy user data from JSON file
#     with open("data/artists.json") as f:
#         user_artists = json.loads(f.read())

#     # Create dummy users, store them in list so we can use them
#     artists_in_db = []
#     for artist in user_artists:
#         sp_artist_id, artist_name = (
#             artist["sp_artist_id"],
#             artist["artist_name"]
#         )
#         db_artists = crud.add_artist(user_id, sp_artist_id, artist_name)
#         dum_artists_in_db.append(db_artists)
#         model.db.session.commit()
    
#     return artists_in_db

def add_artist(user_id, sp_artist_id, artist_name):
    
    artist = Artist(
        sp_artist_id=sp_artist_id, 
        artist_name=artist_name,
        user_id=user_id,
    )
    
    db.session.add(artist)
    db.session.commit()
    
    return artist

def get_user_artists(user_id):
    """Return a list of artists based on user_id."""
    
    top_artists = Artist.query.filter(Artist.user_id == user_id).all()
    
    return top_artists
