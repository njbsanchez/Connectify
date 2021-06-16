"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings")
os.system("createdb ratings")

model.connect_to_db(server.app)
model.db.create_all()

# Load dummy user data from JSON file
with open("data/users.json") as f:
    dummy_data = json.loads(f.read())

# Create dummy users, store them in list so we can use them
dummies_in_db = []
for dummy in dummy_data:
    email, password, name, s_id, lat, long, played_at = (
        dummy["email"],
        dummy["password"],
        dummy["name"],
        dummy["s_id"],
        dummy["latitude"],
        dummy["longitude"]
    )
    last_played = datetime.strptime(dummy["played_at"], "%Y-%m-%dT%H:%M:%S.%f%z")

    db_dummy = crud.create_user(email, password, name, s_id, lat, long, played_at)
    dummies_in_db.append(db_dummy)

dummies_in_db = []
for dummy in dummy_data:
    email, password, name, s_id, lat, long, played_at = (
        dummy["email"],
        dummy["password"],
        dummy["name"],
        dummy["s_id"],
        dummy["latitude"],
        dummy["longitude"]
    )
    last_played = datetime.strptime(dummy["played_at"], "%Y-%m-%dT%H:%M:%S.%f%z")

    db_dummy = crud.create_user(email, password, name, s_id, lat, long, played_at)
    dummies_in_db.append(db_dummy)