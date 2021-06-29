"""Server for playlist profile app."""

from urllib.parse import urlencode

from flask.helpers import send_from_directory
import crud
from model import connect_to_db, db, User, Track, Artist, Playlist, Bookmark
import os
from jinja2 import StrictUndefined
from flask import (
    Flask,
    render_template,
    session,
    request,
    redirect,
    jsonify,
    flash,
    send_from_directory,
)
import json

# from flask_oauth import OAuth
# from spotipy import Spotify, CacheHandler
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
# import spotipy

import spot_api as sp

SPOITFY_CLIENT_ID = sp.SPOITFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET = sp.SPOTIFY_CLIENT_SECRET

app = Flask(__name__)
app.secret_key = "DEV"
app.jinja_env.undefined = StrictUndefined
oauth_manager = SpotifyOAuth(
    client_id=SPOITFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri="http://localhost:5000/auth",
    scope="user-read-email playlist-read-private playlist-read-collaborative user-top-read",
    cache_handler=sp.CacheSessionHandler(session, "spotify_token"))

@app.route("/coming_soon")
def coming_soon():
    """dummy development page"""
    
    return render_template("coming_soon.html")

@app.route("/")
def landing():
    """View Landing page"""
    
    if 'user_id' in session:
        return redirect('/connect')
    
    return render_template("landing.html")

@app.route("/create")
def create_new_account():
    """Show new account form."""
    
    return render_template("create_profile_form.html")

@app.route("/create-user", methods=["POST"])
def register_user():
    """Create a new user."""
    
    email = request.form.get("email")
    password = request.form.get("password")
    name = request.form.get("name")
    s_id = request.form.get("s_id") 
    
    user = crud.get_user_by_email(email)
    
    if user:
        flash("An account already exists for that email. Please sign in or create an account using a different email.")
    else:
        print(email, password, name, s_id)
        crud.create_user(email, password, name, s_id)
    
    return redirect("/") #back to /auth


@app.route("/auth")
def authenticate():
    code = request.args.get('code')
    next = request.args.get('next')

    if code:
        oauth_manager.get_access_token(code)
    
    if oauth_manager.validate_token(oauth_manager.get_cached_token()):
        return redirect(next)


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form["email"]
    password = request.form["password"]
    
    user = crud.get_user_by_email(email)            #check if user exists in database
    
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        session["user_email"] = user.email
        session["user_id"] = user.user_id
        flash(f"Welcome back, {user.name}!")
        return redirect("/connect")
    
    return redirect("/")  #back to auth

@app.route("/profile")
def show_profile():
    
    if "user_id" not in session.keys():
        flash("Please sign in to access your profile.")
        return redirect("/")
    
    print(f"SESSION: {session}")
    
    user_id = session["user_id"]
    if 'code' in request.args:
        oauth_manager.get_access_token(request.args['code'])    
    
    sp_oauth = sp.get_sp_oauth(oauth_manager)
    
    if not sp_oauth:
        flash("Please authenticate your Spotify profile in order to proceed.")

        oauth_manager.redirect_uri = "http://localhost:5000/profile"
        return redirect(oauth_manager.get_authorize_url())
    
    sp_playlists = sp_oauth.current_user_playlists(limit=3)
   
    playlists = []
    
    for playlist in sp_playlists['items']:
        playlist_entry = {'sp_playlist_id':playlist['id'],
                        'playlist_name':playlist['name'],
                       'playlist_desc':playlist['description'],
                       's_id':playlist['owner']['id'],
                       'play_url':playlist['external_urls']['spotify'],
                    #    'href':playlist['external_urls']['href']
                        }
        playlists.append(playlist_entry)
        
    print("************ successfully pulled playlists from spotify and moved to json *******")
    
    for playlist in playlists:
        crud.add_playlist(playlist["sp_playlist_id"], playlist["s_id"], playlist["playlist_name"], playlist["play_url"], playlist["playlist_desc"], user_id)
        
    print("************* successfully uploaded all playlists to current user ************")
    
    sp.update_my_playlists(user_id, oauth_manager)                                   
    sp.update_my_tracks(user_id, oauth_manager)
    sp.update_my_artists(user_id, oauth_manager)
       
    user = crud.get_user_by_id(user_id)
    top_tracks = crud.get_user_tracks(user_id)
    top_artists = crud.get_user_artists(user_id)
    recent_playlists =  crud.get_user_playlists(user_id)
    
    return render_template("profile.html", recent_playlists=recent_playlists, user=user, top_tracks=top_tracks, top_artists=top_artists)









@app.route("/connect")
def connect_users():
    """show map of other users"""
    
    users = crud.get_users()
    current_user = User.query.filter_by(user_id=session["user_id"]).first_or_404()
    
    return render_template("connect.html", users=users, current_user=current_user)

@app.route("/api/usersinfo")
def user_info():
    """JSON information about users info."""
    
    # users_in_db = crud.get_users()
    
    users = [
        {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "s_id": user.s_id,
            "latitude": user.latitude,
            "longitude": user.longitude,
            "recent_activity": user.recent_activity
        }
        for user in User.query.all()
    ]
    return jsonify(users)

@app.route("/api/myinfo")
def my_info():
    """JSON information about users info."""
    
    print(session['user_id'])
    my_info = crud.get_user_by_id(session['user_id'])
    print(my_info)
    
    print("**************************")
    info = [
        {
            "user_id": my_info.user_id,
            "name": my_info.name,
            "email": my_info.email,
            "s_id": my_info.s_id,
            "latitude": my_info.latitude,
            "longitude": my_info.longitude,
            "recent_activity": my_info.recent_activity
        }
    ]
    
    print(info)
    
    return jsonify(info)

@app.route("/api/user/location", methods=["POST"])   #restful api type of web api - way to call a funct; HTTP request to an endpoint
def update_user_location():
    """Update user's lat, long."""
    
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")

    user = crud.get_user_by_id(session["user_id"])
    crud.update_user_location(user, latitude, longitude)
 
    return jsonify({"latitude": user.latitude, "longitude": user.longitude})

@app.route("/home")
def homepage():
    """
    View Homepage - approve access to location.
    """

    user_id = session.get('user_id')
    
    if user_id:
        return render_template("home.html")
    else:
        return redirect("/")

"""under construction ************************************************************************************ """

@app.route('/bookmark/<bookmarked_user_id>/<action>')
def bookmark_action(bookmarked_user_id, action):
    
    current_user = crud.get_user_by_id(session["user_id"])

    # user_to_action = User.query.filter_by(user_id=bookmarked_user_id).first_or_404()
    if action == 'bookmark':
        current_user.bookmark_user(bookmarked_user_id)
        db.session.commit()
    if action == 'unbookmark':
        current_user.unbookmark_user(bookmarked_user_id)
        db.session.commit()
        
    return redirect("/bookmarks")

# @app.route("/bookmark/<int: bookmarked_user_id>/<action>", methods=["POST"])
# def bookmark_action(bookmarked_user_id, action):
    
#     current_user = User.User.query.filter_by(user_id=session["user_id"]).first_or_404()

#     # user_to_action = User.query.filter_by(user_id=bookmarked_user_id).first_or_404()
#     if action == 'bookmark':
#         current_user.bookmark_user(bookmarked_user_id)
#         db.session.commit()
#     if action == 'unbookmark':
#         current_user.unbookmark_user(bookmarked_user_id)
#         db.session.commit()
        
#     return redirect("/bookmarks")

@app.route("/bookmarks")
def see_all_bookmarks():
    
    current_user_id = session["user_id"]

    bookmarks = Bookmark.query.filter_by(user_id=current_user_id).all()
        
    return render_template("bookmarks.html", bookmarks=bookmarks)

"""under construction ************************************************************************************ """
   
@app.route('/logout')
def logout():
    """logout current user"""
    session.clear()
    return redirect('/')

@app.route("/users")
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template("all_users.html", users=users)

@app.route("/bookmarks")
def show_bookmarks():
    """View all bookmarks."""
    
    
    bookmarks = crud.get_all_bookmarks()

    return render_template("bookmarks.html", bookmarks=bookmarks)

@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""

    user = crud.get_user_by_id(user_id)
    top_tracks = crud.get_user_tracks(user_id)
    top_artists = crud.get_user_artists(user_id)
    recent_playlists = crud.get_user_playlists(user_id)
    artist_comparison = crud.compare_artists(session["user_id"],user_id)
    track_comparison = crud.compare_tracks(session["user_id"],user_id)
    artist_count = len(top_artists)
    track_count = len(top_tracks)

    return render_template("user_profile.html", user=user, top_artists=top_artists, top_tracks=top_tracks, recent_playlists=recent_playlists, artist_comparison=artist_comparison, track_comparison=track_comparison, artist_count=artist_count, track_count=track_count)

@app.route("/comparison.json")
def get_comparison_data(user_id):
    """Show details on a particular user."""

    artist_comparison = crud.compare_artists(session["user_id"],user_id)
    track_comparison = crud.compare_tracks(session["user_id"], user_id)

    comparisons = [
        {'type': "Artist", 'ratio':artist_comparison["a_similarity_ratio"]},
        {'type': "Track", 'ratio': track_comparison["t_similarity_ratio"]}
    ]
    
    return jsonify({'data':comparisons})


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()
    app.run(debug=True, use_reloader=True, use_debugger=True)
    

#if you get an error code that says "RuntimeError: application not registered on db instance and no application bound to current context", comment in line 17-20 in modelpy and comment out line 258 and lines 127 & 13 in model.py.