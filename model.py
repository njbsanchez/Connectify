"""models for trackify app"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_to_db(flask_app, db_uri='postgresql:///trackify', echo=False):       #postgresql
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

class User(db.Model):
    """A user."""
    
    __tablename__ = "users"
    
    user_id = db.Column(db.Integer,
                        autoincrement=True, 
                        primary_key=True)
    name = db.Column(db.String, 
                      nullable=False)
    email = db.Column(db.String, 
                      nullable=False, 
                      unique=True)
    password = db.Column(db.String, 
                      nullable=False)
    s_id = db.Column(db.String)
    latitude = db.Column(db.String)
    longitude = db.Column(db.String)
    recent_activity = db.Column(db.DateTime)
      
    def __repr__(self):
        return f'< user_id = {self.user_id} name = {self.name} email = {self.email} >'
    
class Track(db.Model):
    """Top 50 tracks (long term)"""
    
    __tablename__ = "tracks"
    
    track_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    sp_track_id = db.Column(db.String,
                          nullable=False)
    track_name = db.Column(db.String,
                          nullable=False)
    artist_id = db.Column(db.String,
                          nullable=False)
    popularity = db.Column(db.String,
                           nullable=False)
    genre = db.Column(db.String,
                      nullable=False)
    user_id = db.Column(db.ForeignKey('users.user_id'),
                              nullable=True)
    
    track = db.relationship('User', backref='tracks')
    
    def __repr__(self):
        return f'< song_id = {self.track_id} song_name = {self.track_name} >'
    
class Artist(db.Model):
    """An Artist."""
    
    __tablename__ = "artists"
    
    artist_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    sp_artist_id = db.Column(db.String,
                          nullable=False)
    artist_name = db.Column(db.String,
                          nullable=False)
    user_id = db.Column(db.ForeignKey('users.user_id'),
                              nullable=True)

    artist = db.relationship('User', backref='artists')

    #functions here
    
    def __repr__(self):
        return f'< artist_id = {self.artist_id} artist_name = {self.artist_name} >'

class Playlist(db.Model):
    """A playlist."""
    
    
    __tablename__ = "playlists"
    
    playlist_id = db.Column(db.Integer, 
                            autoincrement=True, 
                            primary_key=True)
    sp_playlist_id = db.Column(db.Integer, 
                              nullable=False)
    sp_user_id = db.Column(db.String, 
                             nullable=False)
    playlist_name = db.Column(db.String, 
                              nullable=False)
    user_id = db.Column(db.ForeignKey('users.user_id'),
                              nullable=True)
    
    playlist = db.relationship('User', backref='playlists')

    def __repr__(self):
        return f'< playlist_id = {self.playlist_id} playlist_name = {self.playlist_name} >'



if __name__ == '__main__':
    from server import app
    
    connect_to_db(app)
    db.create_all()
    db.session.commit()