from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import time
import threading
from spotify_status import SpotifyStatus
import os

app = Flask(__name__)
CORS(app)

current_playing = None

def get_current_song_dict():
    global current_playing
    if isinstance(current_playing, str):
        current_playing = None

    curr_song = None
    if current_playing is not None:

        curr_artists = []

        for a in current_playing['artists']:
            curr_artists.append({
                'name': a['name'],
                'link': a['external_urls']['spotify']
            })

        curr_song = {
            'name': current_playing['name'],
            'artists': curr_artists,
            'link': current_playing['external_urls']['spotify'],
            'image': get_current_playing_image()
        }
    return curr_song

@app.route('/')
def index():
    curr_song = get_current_song_dict()
    return render_template('index.html', curr_song = curr_song)

@app.route('/api/<request>/')
def api(request):
    if request == 'current':
        return jsonify(get_current_song_dict())
    else:
        return 'Unknown request'

def combine_list_str(str_list) -> str:
    """
    Combine strings with commas and/or "and"s appropriately.
    
    Args:
        str_list: A list containing the strings to be combined.
    Returns:
        The final output string.
    """
    if len(str_list) == 1:
        return str_list[0]
    if len(str_list) == 2:
        return str_list[0] + ' and ' + str_list[1]

    return_str = ''
    for i in range(len(str_list) - 1):
        if len(str_list) - i == 2:
            return_str += str_list[i] + ', and ' + str_list[i + 1]
        else:
            return_str += str_list[i] + ', '
    return return_str

def get_current_playing_image() -> str:
    """
    Get the currently playing image link.

    Returns:
        The currently playing track's image reference.
    """
    global current_playing
    if current_playing is None:
        return None
    else:
        try:
            return current_playing['album']['images'][0]['url']
        except Exception as e:
            print(e)
            return None

def get_current_playing_string() -> str:
    """
    Get the currently playing track.
    
    Returns:
        The currently playing track in string format.
    """
    global current_playing
    if current_playing is None:
        return "Evan's not listening to anything right now. Maybe later!"
    else:
        song = current_playing['name']
        song_link = current_playing['external_urls']['spotify']
        artists = combine_list_str(['<a href="{}"'.format(a['external_urls']['spotify']) + '>' + a['name'] + '</a>' for a in current_playing['album']['artists']])

        return """
        Evan's listening to <a href="{song_link}">{song}</a> by {artists}.
        """.format(song=song, song_link=song_link, artists=artists)

def update_current_playing():
    global current_playing
    while True:
        current_playing = ss.get_current_playing()
        time.sleep(5)

if __name__ == '__main__':
    ss = SpotifyStatus()
    update_thread = threading.Thread(target=update_current_playing)
    update_thread.start()

    host = '0.0.0.0'
    port = 5002
    
    if 'SPOTIFY_STATUS_CERT' in os.environ and 'SPOTIFY_STATUS_KEY' in os.environ:
        context = (os.getenv('SPOTIFY_STATUS_CERT'), os.getenv('SPOTIFY_STATUS_KEY'))
        app.run(host=host, port=port, ssl_context = context)
    else:
        app.run(host=host, port=port)
