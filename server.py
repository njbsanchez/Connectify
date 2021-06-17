"""Server for playlist profile app."""
import crud
from model import connect_to_db, db, User
import os
from jinja2 import StrictUndefined
import spot_api as sp
from flask import (
    Flask,
    render_template,
    session,
    request,
    redirect,
    jsonify,
    flash
)

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
    redirect_uri="http://localhost:5000/auth",
    scope="user-read-email playlist-read-private playlist-read-collaborative user-top-read",
    cache_handler=CacheSessionHandler(session, "spotify_token"))

connect_to_db(app)
db.create_all()

@app.route("/coming_soon")
def coming_soon():
    """dummy development page"""
    
    return render_template("coming_soon.html")

@app.route("/", methods=["GET"])
def landing():
    """View Landing page"""
    
    # if request.args.get("code") or oauth_manager.validate_token(
    #     oauth_manager.get_cached_token()):
    #     oauth_manager.get_access_token(request.args.get("code"))
    #     flash("Account created! Please log in.")
    #     return redirect("/")
    
    return render_template("landing.html" #, spotify_auth_url=oauth_manager.get_authorize_url()
    )

@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")
    
    user = crud.get_user_by_email(email)            #check if user exists in database
    
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        return redirect ("/")   
    else:
        session["user_email"] = user.email
        session["user_id"] = user.user_id
        flash(f"Welcome back, {user.name}!")
        return redirect("/auth")

@app.route("/create")
def create_new_account():
    """Show new account form."""
    
    return render_template("create_profile_form.html")

@app.route("/create", methods=["POST"])
def register_user():
    """Create a new profile."""
    
    email = request.form.get("email")
    password = request.form.get("password")
    name = request.form.get("name")
    s_id = request.form.get("s_id")
    latitude = request.form.get("password")
    longitude = request.form.get("password")
    played_at = request.form.get("password")   
    
    user = crud.get_user_by_email(email)
    spot_user = crud.get_user_by_spot(s_id)
    
    if user:
        flash("An account already exists for that email. Please sign in or create an account using a different email.")
        return redirect("/")
    elif spot_user:
        flash("An account already exists for that spotify id. Please sign in or create an account using a different spotify id.")
        return redirect("/")
    else:
        crud.create_user(email, password, name, s_id, latitude, longitude, played_at)
        return redirect("/auth")
    

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


@app.route("/profile")
def show_profile():
    
    # if session["user_id"] is None:
    #     flash("Please sign in to access your profile."
    # return redirect ("/")
    # trackify_user = session["user_id"]
    if not oauth_manager.validate_token(oauth_manager.get_cached_token()):
            return redirect("/auth")
    else:
        sp_oauth = Spotify(auth_manager=oauth_manager)
       
    sp_user_info = sp.get_spotify_info

    tracks = sp.get_all_tracks()
    artists = sp.get_my_artists()
    # playlists =  sp.get_my_playlists()
    
    return render_template("profile.html", sp_user_info=sp_user_info, artists=artists, tracks=tracks)

@app.route("/edit_top_playlists")
def edit_top_playlists():
    """
    To edit top 3 playlists displayed on the profile. User can select 3 playlists from a checklist.
    """
    sp_oauth = sp.get_sp_oauth(oauth_manager)
    user_playlists = sp.get_my_playlists()
    return render_template("play.html", spotify=sp_oauth, playlists=user_playlists)



@app.route("/auth")
def authenticate():
    jinja_env = {}

    if request.args.get("code") or oauth_manager.validate_token(
        oauth_manager.get_cached_token()):
        oauth_manager.get_access_token(request.args.get("code"))
        flash("Account created! Please log in.")
        return redirect("/")

    return redirect(jsonify(spotify_auth_url=oauth_manager.get_authorize_url()))



@app.route("/api/usersinfo")
def bear_info():
    """JSON information about users info."""
    
    users_in_db = crud.get_users()

    users_json = [
        {
            "user_id": users_in_db.user_id,
            "name": users_in_db.name,
            "email": users_in_db.email,
            "s_id": users_in_db.s_id,
            "latitude": users_in_db.latitude,
            "longitude": users_in_db.longitude,
            "recent_activity": users_in_db.recent_activity
        }
        for user in users_in_db.query.all()
    ]   
    
    return jsonify(users_json)

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
    
    if session["user_id"] == None:
         return render_template("landing.html")
     
    return render_template("home.html")


@app.route('/logout')
def logout():
    """logout current user"""
    session.clear()
    return redirect('/')

@app.route("/connect")
def connect():
    """show map of other users"""
    
    return render_template("connect.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, use_debugger=True)
    db.create_all()
