"""CRUD operations."""
from model import db, User, connect_to_db #Playlist, Song, Artist,
    
def check_user_by_email()

def create_user(email, password, f_name, l_name, spot_user_id, latitude=00000, longitude=00000, played_at="none"):
    """Create and return a new user."""

    user = User(email=email, password=password, f_name=f_name, l_name=l_name, spot_user_id=spot_user_id)

    db.session.add(user)
    db.session.commit()

    return user

def check_account_by(email):
    """Check if account already exists"""
    
    return User.query.get(user_id)

def create_playlist(email, password, f_name, l_name, spot_user_id):
    """Create and return a new user."""

    user = User(email=email, password=password, f_name=f_name, l_name=l_name, spot_user_id=spot_user_id)

    db.session.add(user)
    db.session.commit()

    return user

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def get_user_by_spot(spot_user_id):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()
