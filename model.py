"""models for trackify app"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""
    
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    email = db.Column(db.String,
                      nullable=False,
                      unique=True)
    password = db.Column(db.String(45),
                         nullable=False)
    f_name = db.Column(db.String(15),
                       nullable=False)
    l_name = db.Column(db.String(35),
                       nullable=False)
    spot_user_id = db.Column(db.String,
                     nullable=False,
                     unique=True)
    latitude = db.Column(db.Float,
                         nullable=True)
    longitude = db.Column(db.Float,
                          nullable=True)
    recent_activity = db.Column(db.DateTime)            #may need to be fixed
    
    def __repr__(self):
        return f'< user_id = {self.user_id} name = {self.f_name} {self.l_name} email = {self.email} >'


# class Playlist(db.Model):
#     """A playlist."""
    
#     playlist_id = db.Column(db.Integer,
#                             autoincrement=True,
#                             primary_key=True)
#     s_playlist_id = db.Column(db.Integer,
#                               nullable=False)
#     top_3playlists = db.Column(db.ForeignKey('Top3List.top_id'),
#                                nullable=True)
#     spot_user_id = db.Column(db.String,
#                             #  db.ForeignKey('User.spot_user_id'),          #do i need this here?
#                              nullable=False)
#     playlist_name = db.Column(db.String,
#                               nullable=False)
    
#     top_3playlists = db.relationship('Top3List', backref='playlists')
    
#     def __repr__(self):
#         return f'< playlist_id = {self.playlist_id} playlist_name = {self.playlist_name} >'
    

# class Top3List:
#     top_id = db.Column(db.Integer,
#                             autoincrement=True,
#                             primary_key=True)
#     user_id = db.Column(db.Integer,
#                         db.ForeignKey('User.user_id'),
#                         nullable=False)
    
#     user = db.relationship('User', backref='top_3list')
    
    
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
    
#     top_song = db.relationship('TopSong', backref='top_songs')
    
#     def __repr__(self):
#         return f'< song_id = {self.song_id} song_name = {self.song_name} >'


# class TopSong:
#     top_song_id = db.Column(db.Integer,
#                             autoincrement=True,
#                             primary_key=True)
#     user_id = db.Column(db.Integer,
#                         db.ForeignKey('User.user_id'),
#                         nullable=False)
    
#     user = db.relationship('User', backref='top_songs')
    
    
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
    
#     top_artist = db.relationship('TopArtist', backref='top_artists')
    
    
#     def __repr__(self):
#         return f'< artist_id = {self.artist_id} artist_name = {self.artist_name} >'


# class TopArtist:
#     top_artist_id = db.Column(db.Integer,
#                             autoincrement=True,
#                             primary_key=True)
#     user_id = db.Column(db.Integer,
#                         db.ForeignKey('User.user_id'),
#                         nullable=False)
    
#     user = db.relationship('User', backref='top_artists')

def connect_to_db(flask_app, db_uri='postgresql:///trackify', echo=True):       #postgresql
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
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