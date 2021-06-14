"""models for trackify app"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""
    
    __tablename__ = "users"
    
    user_id = db.Column(db.Integer,
                        autoincrement=True, 
                        primary_key=True)
    email = db.Column(db.String, 
                      nullable=False, 
                      unique=True)
    password = db.Column(db.String(45), 
                         nullable=False)
    name = db.Column(db.String(50), 
                     nullable=False)
    spot_user_id = db.Column(db.String, 
                             nullable=False, 
                             unique=True)
    latitude = db.Column(db.Float, 
                         nullable=True)
    longitude = db.Column(db.Float, 
                          nullable=True)
    recent_activity = db.Column(db.DateTime)            #may need to be fixed
    
      #functions here
      
    def __repr__(self):
        return f'< user_id = {self.user_id} name = {self.name} email = {self.email} >'


# class Playlist(db.Model):
#     """A playlist."""
    
#     playlist_id = db.Column(db.Integer, 
#                             autoincrement=True, 
#                             primary_key=True)
#     s_playlist_id = db.Column(db.Integer, 
#                               nullable=False)
#     fav_playlist = db.Column(db.ForeignKey('FavPlaylist.fav_id'), 
#                              nullable=True)
#     spot_user_id = db.Column(db.String, 
#                              nullable=False)
#     playlist_name = db.Column(db.String, 
#                               nullable=False)
    
#     #functions here
    
#     fav_playlists = db.relationship('FavPlaylist', backref='playlists')


    
#     def __repr__(self):
#         return f'< playlist_id = {self.playlist_id} playlist_name = {self.playlist_name} >'
    

# class FavPlaylist(db.Model):
#     ""
#     fav_id = db.Column(db.Integer, 
#                        autoincrement=True, 
#                        primary_key=True)
#     user_id = db.Column(db.Integer, 
#                         db.ForeignKey('User.user_id'), 
#                         nullable=False)
    

#     #functions here

#     user = db.relationship('User', backref='fav_playlists')
    
#     def __repr__(self):
#         return f'< playlist_id = {self.playlist_id} playlist_name = {self.playlist_name} >'
    
    
# class Song(db.Model):
#     """A song."""
    
#     song_id = db.Column(db.Integer,
#                         autoincrement=True,
#                         primary_key=True)
#     s_song_id = db.Column(db.String,
#                           nullable=False)
#     song_name = db.Column(db.String,
#                           nullable=False)
#     artist_id = db.Column(db.String,
#                           nullable=False)
#     top_song_id = db.Column(db.ForeignKey('TopSong.top_song_id'),
#                               nullable=True)
    
#         #functions here
    
#     top_song = db.relationship('TopSong', backref='songs')
    
#     def __repr__(self):
#         return f'< song_id = {self.song_id} song_name = {self.song_name} >'


# class TopSong(db.Model):
#     top_song_id = db.Column(db.Integer,
#                             autoincrement=True,
#                             primary_key=True)
#     user_id = db.Column(db.Integer,
#                         db.ForeignKey('User.user_id'),
#                         nullable=False)

#     user = db.relationship('User', backref='top_songs')
   
#     #functions here
    
#     def __repr__(self):
#         return f'< artist_id = {self.top} artist_name = {self.artist_name} >'

    
# class Artist(db.Model):
#     """An Artist."""
    
#     artist_id = db.Column(db.Integer,
#                         autoincrement=True,
#                         primary_key=True)
#     s_artist_id = db.Column(db.String,
#                           nullable=False)
#     artist_name = db.Column(db.String,
#                           nullable=False)
#     top_artist_id = db.Column(db.ForeignKey('TopArtist.top_artist_id'),
#                               nullable=True)
    
#     top_artist = db.relationship('TopArtist', backref='artists')

#     #functions here
    
#     def __repr__(self):
#         return f'< artist_id = {self.artist_id} artist_name = {self.artist_name} >'


# class TopArtist(db.Model):
#     top_artist_id = db.Column(db.Integer,
#                             autoincrement=True,
#                             primary_key=True)
#     user_id = db.Column(db.Integer,
#                         db.ForeignKey('User.user_id'),
#                         nullable=False)
    
#     user = db.relationship('User', backref='top_artists')

#     #functions here
    
#     def __repr__(self):
#         return f'< artist_id = {self.artist_id} artist_name = {self.artist_name} >'


def connect_to_db(flask_app, db_uri='postgresql:///trackify', echo=True):       #postgresql
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app
    
    connect_to_db(app)
    db.create_all()
    db.session.commit()