import spotipy
from spotipy.oauth2 import SpotifyOAuth


def combine_list_str(str_list):
    if len(str_list) == 1:
        return str_list[0]
    if len(str_list) == 2:
        return str_list[0] + ' and ' + str_list[1]
    return_str = ''
    for i in range(len(str_list) - 1):
        if len(str_list) - i == 2:
            return_str += str_list[i] + ' and ' + str_list[i + 1]
        else:
            return_str += str_list[i] + ', '
    return return_str

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="01f1bdc7c6f4481c98c980889567dc17",
                                               client_secret="58ae618c179947e6962e0fa8c54d07dd",
                                               redirect_uri="http://evanshrestha.com",
                                               scope="user-read-currently-playing"))

results = sp.current_user_playing_track()

if results is None:
    print('Not currently playing a track')
else:
    song = results['item']
    title = song['name']
    artists = [a['name'] for a in song['artists']]
    print(f'Now playing {title} by {combine_list_str(artists)}')
