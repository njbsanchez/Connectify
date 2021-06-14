"""CRUD operations."""
from model import db, User, connect_to_db #Playlist, Song, Artist,


def create_user(email, password, name, spot_user_id, latitude=00000, longitude=00000, played_at="none"):
    """Create and return a new user."""

    user = User(email=email, password=password, name=name, spot_user_id=spot_user_id)

    db.session.add(user)
    db.session.commit()

    return user

# def create_playlist(email, password, name, spot_user_id):
#     """Create and return a new user."""

#     user = User(email=email, password=password, name=name, spot_user_id=spot_user_id)

#     db.session.add(user)
#     db.session.commit()

#     return user

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def get_user_by_spot(spot_user_id):
    """Return a user by email."""

    return User.query.filter(User.spot_user_id == spot_user_id).first()
