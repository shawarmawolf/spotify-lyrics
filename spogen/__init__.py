import os
import spotipy
import spotipy.util as util
import lyricsgenius
from flask import Flask, render_template, jsonify


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import lyrics
    objects = lyrics.init(spotipy, util, lyricsgenius)

    @app.route('/_get_music_data')
    def get_music_data():
        current_song_id = lyrics.get_song_data(objects["spotipy"], objects["genius"])
        print("[get_music_data]", "type of song id:", current_song_id)
        song_details = lyrics.print_track(current_song_id)
        return jsonify(songname = song_details[0], lyrics = song_details[1])

    @app.route('/')
    def root():
        return render_template('base.html')

    return app