"""Script to seed database."""

import os
import json
from datetime import datetime

import crud
import model
import server

os.system("dropdb trackify")
os.system("createdb trackify")

print("************************ TRACKIFY DB CREATED ****************")

model.connect_to_db(server.app)
model.db.create_all()

def get_dummies():
    """Load bears from dataset into database."""

    # Load dummy user data from JSON file
    with open("data/profile.json") as f:
        dummy_users = json.loads(f.read())

    # Create dummy users, store them in list so we can use them
    dummies_in_db = []
    for user in dummy_users:
        email, password, name, s_id, lat, long, recent_activity, = (
            user["email"],
            user["password"],
            user["name"],
            user["s_id"],
            user["latitude"],
            user["longitude"],
            user["played_at"]
        )
        last_played = datetime.strptime(user["played_at"], "%Y-%m-%dT%H:%M:%S.%f%z")

        db_user = crud.create_user(email, password, name, s_id, lat, long, recent_activity, last_played)
        dummies_in_db.append(db_user)

    model.db.session.commit()
    

if __name__ == '__main__':
    model.connect_to_db(server.app)
    model.db.create_all()

    get_dummies()