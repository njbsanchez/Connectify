"""Script to seed database."""

import os
import json

from datetime import datetime

import crud
import model
import server

os.system('drop [DATABASE]')
os.system('createdb [DATABASE]')

model.connect_to_db(server.app)
model.db.create_all()

dummy_user ={
    "user_id": "csoledad",
    "email": "csoledad@gmail.com",
    "password": "password",
    "name": "Caesar Soledad",
    "spot_user_id": "124566113",
    "latitude": "12345",
    "longitude": "12345",
    "played_at": "2016-12-13T20:44:04.589Z",  
    }

format = "%Y-%m-%d"
user_id, email, password, name, spot_user_id, latitude, longitude, played_at = (
            dummy_user["user_id"],
            dummy_user["email"],
            dummy_userd[ "password"],
            dummy_user["name"],
            dummy_user["spot_user_id"],
            dummy_user["latitude"],
            dummy_user["longitude"],
            dummy_user["played_at"]        #datetime.strptime( .format)
            )
    
user = crud.create_user(email, password, name, spot_user_id, latitude, longitude, played_at)

# user_id, email, password, name, spot_user_id, latitude, longitude, played_at = (
#             dummy_artist["user_id"],
#             dummy_artist["email"],
#             dummy_artist][ "password"],
#             dummy_artist]["name"],
#             dummy_artist]["spot_user_id"],
#             dummy_artist]["latitude"],
#             dummy_artist]["longitude"],
#             dummy_artist]["played_at"]        #datetime.strptime( .format)
#             )
    
# user = crud.create_user(email, password,name, spot_user_id, latitude, longitude, played_at)

