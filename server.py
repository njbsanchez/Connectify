"""Server for playlist profile app."""
from flask.helpers import send_from_directory
import crud
from model import connect_to_db, db, User
import os
from jinja2 import StrictUndefined
import spot_api as sp
from flask import Flask, render_template, session, request, redirect, jsonify, flash, send_from_directory
import json

# from flask_oauth import OAuth
from spotipy import Spotify, CacheHandler
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import spotipy

SPOITFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

class CacheSessionHandler(CacheHandler):
    def __init__(self, session, token_key):
        self.token_key = token_key
        self.session = session

    def get_cached_token(self):
        print("calling get_cached_token *******************************")
        print(self.session)
        return self.session.get(self.token_key)

    def save_token_to_cache(self, token_info):
        self.session[self.token_key] = token_info
        session.modified = True

app = Flask(__name__)
app.secret_key = "DEV"
app.jinja_env.undefined = StrictUndefined
oauth_manager = SpotifyOAuth(
    client_id=SPOITFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri="http://localhost:5000/profile",
    scope="user-read-email playlist-read-private playlist-read-collaborative user-top-read",
    cache_handler=CacheSessionHandler(session, "spotify_token"))

@app.route("/coming_soon")
def coming_soon():
    """dummy development page"""
    
    return render_template("coming_soon.html")

@app.route("/")
def landing():
    """View Landing page"""
    
    return render_template("landing.html")

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
    
    return redirect("/")   
    

@app.route("/auth")
def authenticate():
    jinja_env = {}

    if request.args.get("code") or oauth_manager.validate_token(oauth_manager.get_cached_token()):
        oauth_manager.get_access_token(request.args.get("code"))
        return redirect("/profile")

    return render_template(
        "index.html", spotify_auth_url=oauth_manager.get_authorize_url()
    )

# @app.route("/auth")
# def authenticate():
#     jinja_env = {}

#     if request.args.get("code") or oauth_manager.validate_token(
#         oauth_manager.get_cached_token()):
#         oauth_manager.get_access_token(request.args.get("code"))
#         flash("Account created! Please log in.")
#         return redirect("/")

#     return redirect(jsonify(spotify_auth_url=oauth_manager.get_authorize_url()))

# @app.route("/api/auth")
# def authen():
#     if request.args.get("code") or oauth_manager.validate_token(
#         oauth_manager.get_cached_token()):
#         oauth_manager.get_access_token(request.args.get("code"))
#         flash("Account created! Please log in.")
#         return redirect("")
    
#     return redirect(jsonify(spotify_auth_url=oauth_manager.get_authorize_url())
      
#     latitude = request.form.get("latitude")
#     longitude = request.form.get("longitude")

#     user = crud.get_user_by_id(session["user_id"])
#     crud.update_user_location(user, latitude, longitude)
 
#     return jsonify({"latitude": user.latitude, "longitude": user.longitude})

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
        crud.create_user(email, password, name, s_id)
        flash("please sign in!")
    
    return redirect("/")


@app.route("/profile")
def show_profile():
    
    if "user_id" not in session.keys():
        flash("Please sign in to access your profile.")
        return redirect("/")
    
    user_id = session["user_id"]
    
    # if not oauth_manager.validate_token(oauth_manager.get_cached_token()):            #this authentication is driving authentication in an endless loop. commented out to allow redirect directly to profile.
    #         return redirect("/p")
    # else:
    #     sp_oauth = Spotify(auth_manager=oauth_manager)
       
    # sp.update_my_playlists(user_id)                                   #to add a "refresh spotify information" button to profile. This updates json with most recent snapshot of track/playlist/artist info.
    # # sp.update_my_tracks(user_id)
    # sp.update_my_artists(user_id)
       
    user = crud.get_user_by_id(user_id)
    top_tracks = crud.get_user_tracks(user_id)
    top_artists = crud.get_user_artists(user_id)
    recent_playlists =  crud.get_user_playlists(user_id)
    
    return render_template("profile.html", recent_playlists=recent_playlists, top_tracks=top_tracks, top_artists=top_artists, user=user) #, top_tracks=top_tracks, top_artists=top_artists)


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
     
    
@app.route('/logout')
def logout():
    """logout current user"""
    session.clear()
    return redirect('/')

@app.route("/connect")
def connect_users():
    """show map of other users"""
    
    users = crud.get_users()
    
    return render_template("connect.html", users=users)

@app.route("/users")
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template("all_users.html", users=users)

@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""

    user = crud.get_user_by_id(user_id)
    top_tracks = crud.get_user_tracks(user_id)
    top_artists = crud.get_user_artists(user_id)
    recent_playlists = crud.get_user_playlists(user_id)
    artist_comparison = crud.compare_artists(session["user_id"],user_id)
    track_comparison = crud.compare_tracks(session["user_id"],user_id)

    return render_template("user_profile.html", user=user, top_artists=top_artists, top_tracks=top_tracks, recent_playlists=recent_playlists, artist_comparison=artist_comparison, track_comparison=track_comparison)

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