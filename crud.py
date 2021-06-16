"""CRUD operations."""
from model import db, User, connect_to_db #Playlist, Song, Artist,

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

# def save_top_3_playlists()