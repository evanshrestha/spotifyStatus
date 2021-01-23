import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

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
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                                               scope="user-read-currently-playing,user-read-recently-played,user-read-playback-state",
                                               open_browser=False))
    def get_current_playing(self):
        results = self.sp.currently_playing()

        if results is None:
            return 'Not currently playing a track'
        else:
            song = results['item']
            return song
            # title = song['name']
            # artists = [a['name'] for a in song['artists']]
            # return f'Now playing {title} by {combine_list_str(artists)}'
    
    def get_recently_played(self):
        results = self.sp.current_user_recently_played()
        song_list = []
        #return_str = ''
        if results is None:
            return_str = 'No recent tracks'
        else:
            for item in results['items']:
                song_list.append(item)
                #return_str += (item['track']['name'] + ' by ' + combine_list_str([a['name'] for a in item['track']['artists']])) + '\n'
        #return return_str
        return song_list

def main():
    ss = SpotifyStatus()
    while True:
        print(ss.get_current_playing())
        time.sleep(60)

if __name__ == '__main__':
    main()
