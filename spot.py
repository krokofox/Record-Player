import json 
import spotipy 
import webbrowser
from spotipy.oauth2 import SpotifyOAuth


# oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri) 
# token_dict = oauth_object.get_access_token() 
# token = token_dict['access_token'] 
# spotifyObject = spotipy.Spotify(auth=token) 
# user_name = spotifyObject.current_user() 
username = 'kcoda36'
clientID = 'c0e306fda7564575b2b8173ad25de008'
clientSecret = '0931a81a50244acf8aa230ff2d968b3e'
redirect_uri = 'http://localhost:8888/callback'
scope = "user-read-currently-playing"



def get_current_playing_info():
    global spotify
    # username = 'kcoda36'
    # clientID = 'c0e306fda7564575b2b8173ad25de008'
    # clientSecret = '0931a81a50244acf8aa230ff2d968b3e'
    # redirect_uri = 'http://localhost:8888/callback'
    # scope = "user-read-currently-playing"
    # oauth_object = SpotifyOAuth(clientID, clientSecret, redirect_uri, scope=scope, username=username)
    # token_info = oauth_object.get_access_token()
    # spotify = spotipy.Spotify(auth=token_info['access_token'])
    
    current_track = spotify.current_user_playing_track()
    if current_track is None:
        return None  # Return None if no track is playing

    # Extracting necessary details
    artist_name = current_track['item']['artists'][0]['name']
    album_name = current_track['item']['album']['name']
    album_cover_url = current_track['item']['album']['images'][0]['url']
    track_title = current_track['item']['name']  # Get the track name

    return {
        "artist": artist_name,
        "album": album_name,
        "album_cover": album_cover_url,
        "title": track_title
    }


def spotify_authenticate(client_id, client_secret, redirect_uri, username):
    # OAuth with the required scopes for playback control and reading currently playing track
    scope = "user-read-currently-playing user-modify-playback-state"
    auth_manager = SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope, username=username)
    return spotipy.Spotify(auth_manager=auth_manager)


spotify = spotify_authenticate(clientID, clientSecret, redirect_uri, username)

def start_music():
    global spotify
    # Start or resume playback on the user's active device
    try:
        spotify.start_playback()
    except spotipy.SpotifyException as e:
        return f"Error in starting playback: {str(e)}"

def stop_music():
    global spotify

    # Pause playback on the user's active device
    try:
        spotify.pause_playback()
    except spotipy.SpotifyException as e:
        return f"Error in stopping playback: {str(e)}"

def skip_to_next():
    global spotify
    # Skip to the next track in the user's queue
    try:
        spotify.next_track()
        return "Skipped to next track."
    except spotipy.SpotifyException as e:
        return f"Error in skipping to next track: {str(e)}"

def skip_to_previous():
    global spotify
    # Skip to the previous track in the user's queue
    try:
        spotify.previous_track()
        return "Skipped to previous track."
    except spotipy.SpotifyException as e:
        return f"Error in skipping to previous track: {str(e)}"

# print(get_current_playing_info(username, clientID, clientSecret, redirect_uri))

# spotify = spotify_authenticate(clientID, clientSecret, redirect_uri, username)
# print(skip_to_previous(spotify))   # Stop music