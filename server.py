"""Server for playlist profile app."""
import os
import crud      
import model
# import spot_api

from flask import (Flask, 
                   render_template, 
                   request, 
                   flash, 
                   session, 
                   redirect,
                   url_for,
)

from model import connect_to_db

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


#----spotipy/spotify api----#
from spotipy import Spotify, CacheHandler
from spotipy.oauth2 import SpotifyOAuth

SPOITFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

class CacheSessionHandler(CacheHandler):
    def __init__(self, session, token_key):
        self.token_key = token_key
        self.session = session

    def get_cached_token(self):
        return self.session.get(self.token_key)

    def save_token_to_cache(self, token_info):
        self.session[self.token_key] = token_info
        session.modified = True
        
oauth_manager = SpotifyOAuth(
    client_id=SPOITFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri="http://localhost:5000",
    scope="user-read-email playlist-read-private playlist-read-collaborative",
    cache_handler=CacheSessionHandler(session, "spotify_token"),
)

connect_to_db(app)
model.db.create_all()

@app.route("/coming_soon")
def coming_soon():
    """dummy development page"""
    
    return render_template("coming_soon.html")

@app.route("/")
def landing():
    """View Landing page"""
    
    return render_template("landing.html")

@app.route("/new_profile_form")
def create_new_account():
    """Show new account form."""
    
    return render_template(
        "new_profile_form.html", spotify_auth_url=oauth_manager.get_authorize_url()
        )


@app.route("/create", methods=["POST"])
def register_user():
    """Create a new profile."""
    
    email = request.form.get("email")
    password = request.form.get("password")
    name = request.form.get("name")
    spot_user_id = request.form.get("spot_user_id")
    latitude = request.form.get("password")
    longitude = request.form.get("password")
    played_at = request.form.get("password")   
    
    user = crud.get_user_by_email(email)
    spot_user = crud.get_user_by_spot(spot_user_id)
    
    if user:
        flash("An account already exists for that email. Please sign in or create an account using a different email.")
        return redirect("/")
    elif spot_user:
        flash("An account already exists for that spotify id. Please sign in or create an account using a different spotify id.")
        return redirect("/")
    else:
        crud.create_user(email, password, name, spot_user_id, latitude, longitude, played_at)
        return redirect("/auth")
    

@app.route("/auth")
def authenticate():
    jinja_env = {}

    if request.args.get("code") or oauth_manager.validate_token(
        oauth_manager.get_cached_token()
    ):
        oauth_manager.get_access_token(request.args.get("code"))
        flash("Account created! Please log in.")
        return redirect("/")

    return render_template(
        "index.html", spotify_auth_url=oauth_manager.get_authorize_url()
    )

@app.route("/spotify-info")
def show_spotify_info():
    if not oauth_manager.validate_token(oauth_manager.get_cached_token()):
        return redirect("/")

    sp = Spotify(auth_manager=oauth_manager)

    return render_template("profile.html", spotify=sp)


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")
    
    user = crud.get_user_by_email(email)            #check if user exists in database
    
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        session["user_email"] = user.email
        session["user_id"] = user.user_id
        flash(f"Welcome back, {user.name}!")

    return redirect("/home")

@app.route("/home")
def homepage():
    """View Homepage"""
    
    return render_template("home.html")

@app.route("/profile")
def user_profile():
    "View user's own profile."


    return render_template("profile.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, use_debugger=True)
    model.db.create_all()
    
    
    # @app.route("/log_out")
# def log_out():
#     """Log out of account."""
#     s = requests.session()
#     s.cookies.clear()
    
#     return redirect("/")