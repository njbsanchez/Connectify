"""CRUD operations."""
from model import db, User, connect_to_db, Playlist, Track, Artist, Bookmark
from flask import session
import random
import argparse
import logging


def create_user(email, name, s_id, latitude=None, longitude=None, recent_activity=None):
    """Create and return a new user."""

    user = User(email=email, name=name, s_id=s_id, latitude=latitude, longitude=longitude, recent_activity=recent_activity)

    db.session.add(user)
    db.session.commit()

    return user

def update_user_with_spotinfo(s_id, recent_activity=None):
    """update user spotify info."""
    
    user = crud.get_user_by_id(session["user_id"])
    
    user.s_id = s_id
    user.recent_activity = recent_activity
    
    db.session.commit()

def update_user_location(user, latitude, longitude):
    """Update user's latitude and longitude."""

    user.latitude = latitude
    user.longitude = longitude

    db.session.add(user)
    db.session.commit()

    return user

def get_sid_by_id(id):
    """Return a user by id."""

    user = User.query.filter(User.user_id == id).first()

    return user.s_id

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

def add_playlist(sp_playlist_id, s_id, playlist_name, play_url, play_desc, user_id):
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
    
    return Playlist.query.filter(Playlist.s_id == s_id).first()

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

def get_user_tracks(user_id):
    """Return a list of artists based on user_id."""
    
    top_tracks = Track.query.filter(Track.user_id == user_id).all()
    
    return top_tracks

def get_user_playlists(user_id):
    """Return a list of artists based on user_id."""
    
    recent_playlists = Playlist.query.filter(Playlist.user_id == user_id).all()
    
    return recent_playlists

def compare_artists(current_user, user_to_compare):
    """."""
    
    current_user = current_user
    user_to_compare = user_to_compare
    
    
    my_artists = Artist.query.filter(Artist.user_id == current_user).all()
    my_set = set()
    
    for artist in my_artists:
        artist_tup = (artist.artist_name, artist.sp_artist_id)
        my_set.add(artist_tup)
        
    user_artists = Artist.query.filter(Artist.user_id == user_to_compare).all()
    user_set = set()
    
    for artist in user_artists:
        artist_tup = (artist.artist_name, artist.sp_artist_id)
        user_set.add(artist_tup)
        
    count = len(my_set & user_set)
    my_artists_to_share = my_set - user_set
    new_artists_to_me = user_set - my_set
    new_artists_3 = set(random.choices(list(new_artists_to_me), k=3))
    artist_similar = set(random.choices(list(my_set & user_set), k=3))  
    count_similar = len(artist_similar)
    if count_similar == 0:
        similarity_ratio = 0
    else:
        similarity_ratio = (count / len(my_set))*100
    if similarity_ratio >= 70:
        similarity_cat = "high"
    elif similarity_ratio >= 40 and similarity_ratio < 70:
        similarity_cat = "med"
    elif similarity_ratio >= 10 and similarity_ratio < 40:
        similarity_cat = "low"
    else:
        similarity_cat = "nada"
    
    artist_comparison = {
        "my_artists_to_share": my_artists_to_share,
        "new_artists_to_me": new_artists_3,
        "artist_similar": artist_similar,
        "count_similar": count_similar,
        "similarity_ratio": similarity_ratio,
        "similarity_cat": similarity_cat
    }
    
    return artist_comparison

def compare_tracks(current_user, user_to_compare):
    """Return a list of artists based on user_id."""
    
    current_user = current_user
    user_to_compare = user_to_compare
    
    my_tracks = Track.query.filter(Track.user_id == current_user).all()
    my_set = set()
    
    for track in my_tracks:
        track_tup = (track.track_name, track.sp_track_id)
        my_set.add(track_tup)
    
    user_tracks = Track.query.filter(Track.user_id == user_to_compare).all()
    user_set = set()
    
    for track in user_tracks:
        track_tup = (track.track_name, track.sp_track_id)
        user_set.add(track_tup)
    
    count = len(my_set & user_set)
    my_tracks_to_share = my_set - user_set
    new_tracks_to_me = user_set - my_set
    new_tracks_3 = set(random.choices(list(new_tracks_to_me), k=3))
    track_similar = set(random.choices(list(my_set & user_set), k=3))  
    count_similar = len(track_similar)
    if count_similar == 0:
            similarity_ratio = 0
    else:
        similarity_ratio = (count / len(my_set)*100)
    if similarity_ratio >= 70:
        similarity_cat = "high"
    elif similarity_ratio >= 40 and similarity_ratio < 70:
        similarity_cat = "med"
    elif similarity_ratio >= 10 and similarity_ratio < 40:
        similarity_cat = "low"
    else:
        similarity_cat = "nada"
    
    track_comparison = {
        "my_tracks_to_share": my_tracks_to_share,
        "new_tracks_to_me": new_tracks_3,
        "track_similar": track_similar,
        "count_similar": count_similar,
        "similarity_ratio": similarity_ratio,
        "similarity_cat": similarity_cat
    }
    
    return track_comparison

def clear_playlists():
    to_delete = get_user_playlists(session["user_id"])
    for playlist in to_delete:
        db.session.delete(playlist)
    db.session.commit()

def clear_tracks():
    to_delete = get_user_tracks(session["user_id"])
    for track in to_delete:
        db.session.delete(track)
    db.session.commit()

def clear_artists():
    to_delete = get_user_artists(session["user_id"])
    for artist in to_delete:
        db.session.delete(artist)
    db.session.commit()
    
def create_bookmark(bookmarked_user_id):
    
    user_id = session['user_id']
    
    bookmark = Bookmark(
        user_id=user_id,
        bookmarked_user_id=bookmarked_user_id)
    
    db.session.add(bookmark)
    db.session.commit()

def delete_bookmark(bookmarked_user_id):
    
    to_delete = get_bookmark(bookmarked_user_id)
    
    db.session.delete(to_delete)
    db.session.commit()
    
def get_bookmark(bookmarked_user_id):
    
    return Bookmark.query.filter(Bookmark.bookmarked_user_id == bookmarked_user_id).first()

def get_all_bookmarks():
    
    return Bookmark.query.filter(Bookmark.user_id == session['user_id']).all()

def create_playlist(sp_playlist_id, s_id, playlist_name, user_id, play_url, play_desc="A Playlist."):

    playlist = Playlist(
        s_id=s_id,
        sp_playlist_id=sp_playlist_id,
        playlist_name=playlist_name, 
        user_id=user_id, 
        play_desc=play_desc, 
        play_url=play_url
    )
    
    db.session.add(playlist)
    db.session.commit()
    
    playlist = Playlist.query.filter(Playlist.sp_playlist_id == sp_playlist_id).first()
    
    return playlist
    
    