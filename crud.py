"""CRUD operations."""
from model import db, User, connect_to_db, Playlist, Track, Artist

def create_user(email, password, name, spot_user_id, latitude=00000, longitude=00000, played_at="none"):
    """Create and return a new user."""

    user = User(email=email, password=password, name=name, spot_user_id=spot_user_id)

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

def get_user_by_spot(spot_user_id):
    """Return a user by email."""

    return User.query.filter(User.spot_user_id == spot_user_id).first()

def get_users():
    """Return all users."""

    return User.query.all()

def add_track(track_name, sp_track_id, artist, artist_id, popularity, genres, user_id):
    track = Track(
        track_name=track_name,
        sp_track_id=sp_track_id,
        artist=artist,
        artist_id=artist_id, 
        popularity=popularity, 
        # genres=genres,
        user_id=user_id
    )
    
    db.session.add(track)
    db.session.commit()
    
    return track

def add_artist(sp_artist_id, artist_name, genre, popularity, image, user_id):
    artist = Artist(
        sp_artist_id=sp_artist_id, 
        artist_name=artist_name,
        # genre=genre,
        popularity=popularity, 
        image=image,
        user_id=user_id,
    )
    
    db.session.add(artist)
    db.session.commit()
    
    return artist