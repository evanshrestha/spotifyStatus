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
            return_str += str_list[i] + ', and ' + str_list[i + 1]
        else:
            return_str += str_list[i] + ', '
    return return_str

class SpotifyStatus:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(redirect_uri="http://evanshrestha.com",
                                               scope="user-read-currently-playing",
                                               open_browser=False))
    def get_current_playing(self):
        results = self.sp.current_user_playing_track()

        if results is None:
            return 'Not currently playing a track'
        else:
            song = results['item']
            title = song['name']
            artists = [a['name'] for a in song['artists']]
            return f'Now playing {title} by {combine_list_str(artists)}'

def main():
    ss = SpotifyStatus()
    print(ss.get_current_playing())

if __name__ == '__main__':
    main()
