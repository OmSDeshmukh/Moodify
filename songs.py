import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Accessing environment variables
spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

# Authenticate with Spotify API
auth_manager = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Search for tracks
track_name = 'Shape of You'
results = sp.search(q=track_name, type='track')

# Print track details
for track in results['tracks']['items']:
    print(f"Track: {track['name']}")
    print(f"Artists: {', '.join([artist['name'] for artist in track['artists']])}")
    print(f"Preview URL: {track['preview_url']}")