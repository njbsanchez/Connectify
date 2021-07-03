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
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

# import spotipy

import spot_api as sp
from create_playlist import SpotifyClient

SPOITFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

app = Flask(__name__)
app.secret_key = "DEV"
app.jinja_env.undefined = StrictUndefined
client_credentials_manager = SpotifyClientCredentials(
    client_id=SPOITFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET
)
oauth_manager = SpotifyOAuth(
    client_id=SPOITFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri="http://localhost:5000/spotify-callback",
    scope="user-read-email playlist-read-private playlist-modify-public playlist-modify-private playlist-read-collaborative user-top-read",
    cache_handler=sp.CacheSessionHandler(session, "spotify_token_info"),
)
spotify = Spotify(auth_manager=oauth_manager)
spotify_cred = Spotify(client_credentials_manager=client_credentials_manager)


@app.route("/coming_soon")
def coming_soon():
    """dummy development page"""

    return render_template("coming_soon.html")


@app.route("/")
def landing():
    """View Landing page"""

    if "user_id" in session and "spotify_token_info" in session:
        return redirect("/connect")

    return render_template("landing.html")


@app.route("/login-with-spotify", methods=["POST"])
def redirect_to_spotify_auth():
    """# should_remember = request.args.get("remember_me")
    # set session to permanent (will cause session to last for 31 days)
    # session.permanent = True"""
    remember_me = request.args.get("remember-me")
    if remember_me:
        session.permanent = True

    return redirect(oauth_manager.get_authorize_url())


@app.route("/spotify-callback")
def handle_redirect_after_spotify_auth():
    "Checks if authentication was provided by user. If approved, code checks if user exists in db and saves user to session.. If not, creates a user and saves to session. "

    spotify_cred = Spotify(
        client_credentials_manager=client_credentials_manager
    )
    code = request.args.get("code")

    if not code:
        alert(
            "Spotify Authentication is required in order to access the app. Please try again."
        )
        return redirect("/")

    oauth_manager.get_access_token(code, check_cache=False)
    spotify_user_info = spotify.current_user()
    print(spotify_user_info)

    user = User.query.filter_by(email=spotify_user_info["email"]).first()

    if not user:
        name = spotify_user_info["display_name"]
        s_id = spotify_user_info["id"]
        email = spotify_user_info["email"]
        photo = spotify_user_info["images"][0]["url"]

        crud.create_user(email, name, s_id, photo)
        return redirect("/profile")

    session["user_id"] = user.user_id

    return redirect("/connect")


@app.route("/profile")
def show_profile():

    if "user_id" not in session.keys():
        flash("Please sign in to access your profile.")
        return redirect("/")

    print(f"SESSION: {session}")

    user_id = session["user_id"]

    sp_playlists = spotify.current_user_playlists(limit=3)

    playlists = []

    for playlist in sp_playlists["items"]:
        playlist_entry = {
            "sp_playlist_id": playlist["id"],
            "playlist_name": playlist["name"],
            "playlist_desc": playlist["description"],
            "s_id": playlist["owner"]["id"],
            "play_url": playlist["external_urls"]["spotify"],
            #    'href':playlist['external_urls']['href']
        }
        playlists.append(playlist_entry)

    print(
        "************ successfully pulled playlists from spotify and moved to json *******"
    )

    for playlist in playlists:
        crud.add_playlist(
            playlist["sp_playlist_id"],
            playlist["s_id"],
            playlist["playlist_name"],
            playlist["play_url"],
            playlist["playlist_desc"],
            user_id,
        )

    print(
        "************* successfully uploaded all playlists to current user ************"
    )

    sp.update_my_playlists(user_id, spotify)
    sp.update_my_tracks(user_id, spotify)
    sp.update_my_artists(user_id, spotify)

    user = crud.get_user_by_id(user_id)
    top_tracks = crud.get_user_tracks(user_id)
    top_artists = crud.get_user_artists(user_id)
    recent_playlists = crud.get_user_playlists(user_id)

    return render_template(
        "profile.html",
        recent_playlists=recent_playlists,
        user=user,
        top_tracks=top_tracks,
        top_artists=top_artists,
    )


@app.route("/connect")
def connect_users():
    """show map of other users"""

    users = crud.get_users()
    current_user = User.query.filter_by(
        user_id=session["user_id"]
    ).first_or_404()
    
    # connect_info = {}
    
    # for user in users:
    #     spotify_cred = spotify_cred.user(user.s_id)
    #     connectify_info[user.user_id]=

    return render_template(
        "connect.html", users=users, current_user=current_user)


@app.route("/api/usersinfo")
def user_info():
    """JSON information about users info."""

    users = [
        {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "s_id": user.s_id,
            "latitude": user.latitude,
            "longitude": user.longitude,
            "recent_activity": user.recent_activity,
        }
        for user in User.query.all()
    ]
    return jsonify(users)


@app.route("/api/myinfo")
def my_info():
    """JSON information about users info."""

    print(session["user_id"])
    my_info = crud.get_user_by_id(session["user_id"])
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
            "recent_activity": my_info.recent_activity,
        }
    ]

    print(info)

    return jsonify(info)


@app.route(
    "/api/user/location", methods=["POST"]
)  # restful api type of web api - way to call a funct; HTTP request to an endpoint
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

    user_id = session.get("user_id")

    if user_id:
        return render_template("home.html")
    else:
        return redirect("/")


@app.route("/bookmark/<bookmarked_user_id>/<action>")
def bookmark_action(bookmarked_user_id, action):

    current_user = crud.get_user_by_id(session["user_id"])

    # user_to_action = User.query.filter_by(user_id=bookmarked_user_id).first_or_404()
    if action == "bookmark":
        current_user.bookmark_user(bookmarked_user_id)
        db.session.commit()
    if action == "unbookmark":
        current_user.unbookmark_user(bookmarked_user_id)
        db.session.commit()

    return redirect("/bookmarks")


@app.route("/create-playlist/<similarity_cat>")
def show_playlist_creator(similarity_cat):
    tracks = []
    bookmarked_users = []
    bookmarks = crud.get_all_bookmarks()

    for bookmark in bookmarks:
        track_comparison = crud.compare_tracks(
            bookmark.user_id, bookmark.bookmarked_user_id
        )
        bookmarked_users.append(bookmark)
        for track in crud.get_user_tracks(bookmark.bookmarked_user_id):
            tracks.append(track)

    return render_template("create_playlist.html", tracks=tracks)


@app.route("/create-playlist/<similarity_cat>", methods=["POST"])
def create_playlist(similarity_cat):

    tracks = []
    bookmarked_users = []
    bookmarks = crud.get_all_bookmarks()

    for bookmark in bookmarks:
        track_comparison = crud.compare_tracks(
            bookmark.user_id, bookmark.bookmarked_user_id
        )
        bookmarked_users.append(bookmark)
        for track in crud.get_user_tracks(bookmark.bookmarked_user_id):
            tracks.append(track)

    playlist_name = request.form.get("playlist_name")
    tok = session["spotify_token_info"].get("access_token")
    # print(tok, "********************** THIS IS TOK")
    spotify_client = SpotifyClient(tok, crud.get_sid_by_id(session["user_id"]))
    playlist = spotify_client.create_playlist(playlist_name)
    print(f"Playlist '{playlist_name}' was created successfully.")
    print(playlist, "#            ##################################")
    spotify_client.populate_playlist(playlist, tracks)
    print(f"Tracks were successfully uploaded to playlist '{playlist_name}'.")
    current_user = crud.get_user_by_id(session["user_id"])

    return redirect("created")


@app.route("/bookmarks")
def see_all_bookmarks():

    current_user = crud.get_user_by_id(session["user_id"])

    bookmarks = crud.get_all_bookmarks()

    # sim_by_artist = {"high", "med", "low", "nada"}
    sim_by_track = {}
    sim_by_track["high"] = []
    sim_by_track["med"] = []
    sim_by_track["low"] = []
    sim_by_track["nada"] = []

    sim_by_artist = {}
    sim_by_artist["high"] = []
    sim_by_artist["med"] = []
    sim_by_artist["low"] = []
    sim_by_artist["nada"] = []

    artists = {}
    artists["high"] = []
    artists["med"] = []
    artists["low"] = []
    artists["nada"] = []

    tracks = {}
    tracks["high"] = []
    tracks["med"] = []
    tracks["low"] = []
    tracks["nada"] = []

    for bookmark in bookmarks:

        bookmarked_user_id = bookmark.bookmarked_user_id
        user_id = bookmark.user_id

        track_comparison = crud.compare_tracks(user_id, bookmarked_user_id)

        sim_by_track[track_comparison["similarity_cat"]].append(bookmark)

        for track in crud.get_user_tracks(bookmarked_user_id):
            tracks[track_comparison["similarity_cat"]].append(track)

        artist_comparison = crud.compare_artists(user_id, bookmarked_user_id)

        sim_by_artist[artist_comparison["similarity_cat"]].append(bookmark)

        for artist in crud.get_user_artists(bookmarked_user_id):
            artists[artist_comparison["similarity_cat"]].append(artist)

    """Playlists created"""

    return render_template(
        "bookmarks.html",
        bookmarks=bookmarks,
        sim_by_track=sim_by_track,
        current_user=current_user,
        artists=artists,
        tracks=tracks,
    )


# topsts.append(playlist)


@app.route("/logout")
def logout():
    """logout current user"""
    session.clear()
    return redirect("/")


@app.route("/users")
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template("all_users.html", users=users)


@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""

    current_user = crud.get_user_by_id(session["user_id"])
    user = crud.get_user_by_id(user_id)
    spotify_user = spotify_cred.user(user.s_id)
    top_tracks = crud.get_user_tracks(user_id)
    top_artists = crud.get_user_artists(user_id)
    
    artists = Artist.query.filter(Artist.user_id == user_id).limit(5)
    artists_sp_info = []
    for artist in artists:
        artist_info = spotify_cred.artist(artist.sp_artist_id)
        artists_sp_info.append(artist_info)

    artist_comparison = crud.compare_artists(session["user_id"], user_id)
    track_comparison = crud.compare_tracks(session["user_id"], user_id)
    
    similar_tracks= []
    for track_name, sp_track_id in track_comparison["track_similar"]:
        track_info = spotify_cred.track(sp_track_id)
        similar_tracks.append(track_info)
    
    new_tracks= []
    for track_name, sp_track_id in track_comparison["new_tracks_to_me"]:
        track_info = spotify_cred.track(sp_track_id)
        new_tracks.append(track_info) 
    
    artist_count = len(top_artists)
    track_count = len(top_tracks)
    playlist_dict = spotify_cred.user_playlists(user.s_id)
    playlists = playlist_dict["items"][:3]
    num_playlists = len(playlist_dict["items"])
    avg_ratio = (
        artist_comparison["similarity_ratio"]
        + track_comparison["similarity_ratio"]
    ) / 2
    return render_template(
        "user_profile.html",
        num_playlists=num_playlists,
        user=user,
        current_user=current_user,
        top_artists=top_artists,
        artists_sp_info=artists_sp_info,
        spotify_user=spotify_user,
        top_tracks=top_tracks,
        artist_comparison=artist_comparison,
        track_comparison=track_comparison,
        artist_count=artist_count,
        track_count=track_count,
        playlists=playlists,
        avg_ratio=avg_ratio,
        similar_tracks=similar_tracks,
        new_tracks=new_tracks
    )


@app.route("/comparison.json")
def get_comparison_data(user_id):
    """Show details on a particular user."""

    artist_comparison = crud.compare_artists(session["user_id"], user_id)
    track_comparison = crud.compare_tracks(session["user_id"], user_id)

    comparisons = [
        {"type": "Artist", "ratio": artist_comparison["a_similarity_ratio"]},
        {"type": "Track", "ratio": track_comparison["t_similarity_ratio"]},
    ]

    return jsonify({"data": comparisons})


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()
    app.run(debug=True, use_reloader=True, use_debugger=True)


# if you get an error code that says "RuntimeError: application not registered on db instance and no application bound to current context", comment in line 17-20 in modelpy and comment out line 258 and lines 127 & 13 in model.py.
