"""Server for playlist profile app."""

from flask import Flask, render_template, request, flash, session, redirect
from  model import connect_to_db
import crud      
# from jinja import StrictUndefined #disallows all operations beside testing if it’s an undefined object.

app = Flask(__name__)

# routes and view functions go here

@app.route("/")
def homepage():
    """View Homepage"""
    
    return render_template("homepage.html")

@app.route("/new_profile_form")
def redirect():
    """Show new account form."""
    
    return render_template("new_profile_form.html")

@app.route("/create", methods=["POST"])
def register_user():
    """Create a new profile."""
    
    email = request.form.get("email")
    password = request.form.get("password")
    f_name = request.form.get("password")
    l_name = request.form.get("password")
    spot_user_id = request.form.get("password")
    latitude = request.form.get("password")
    longitude = request.form.get("password")
    played_at = request.form.get("password")   
    
    user = crud.get_by_email(email)
    spot_user = crud.get_by_spot(spot_user_id)
    
    if user:
        flash("An account already exists for that email. Please sign in or create an account using a different email.")
    elif spot_user:
        flash("An account already exists for that spotify id. Please sign in or create an account using a different spotify id.")
    else:
        crud.create_user(email, password, f_name, l_name, spot_user_id, latitude, longitude, played_at)
        flash("Account created! Please log in.")
    return redirect("/") 

# @app.route("/login", methods=["POST"])
# def process_login():
#     """Process user login."""

#     email = request.form.get("email")
#     password = request.form.get("password")

#     user = crud.get_user_by_email(email)
#     if not user or user.password != password:
#         flash("The email or password you entered was incorrect.")
#     else:
#         # Log in user by storing the user's email in session
#         session["user_email"] = user.email
#         flash(f"Welcome back, {user.email}!")

#     return redirect("/")

# @app.route("/profile")
# def user_profile():
#     "View user's own profile."
    
#      user = crud.get_user_by_id(user_id)
    
#     return render_template("profile.html")


#     return redirect("/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)