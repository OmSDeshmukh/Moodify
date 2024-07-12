import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from dotenv import load_dotenv
import os
from pprint import pprint
import json

from tone_analyser import get_emotion

# Load environment variables from .env file
load_dotenv()

# Accessing environment variables
spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

# Authenticate with Spotify API
auth_manager = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Check if the variables are loaded correctly
if not spotify_client_id or not spotify_client_secret:
    raise ValueError("Spotify client ID or secret not found in environment variables.")

# Authenticate with Spotify API
try:
    auth_manager = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
except Exception as e:
    print(f"Authentication failed: {e}")
    
    
# Search for tracks
# track_name = 'Shape of You'
# results = sp.search(q=track_name, type='track')

# # Print track details
# for track in results['tracks']['items']:
#     print(f"Track: {track['name']}")
#     print(f"Artists: {', '.join([artist['name'] for artist in track['artists']])}")
#     print(f"Preview URL: {track['preview_url']}")

def mood_genre_mapping(emotion):
    recommended_songs = []

    # Define genre mappings for each emotion
    genre = {
        'joy': ["happy", "pop", "dance"],
        'sadness': ["sad", "acoustic", "ballads"],
        'anger': ["rock", "metal", "punk"],
        'fear': ["dark ambient", "suspense"],
        'surprise': ["experimental", "indie"],
        'disgust': ["avant-garde", "alternative"],
        'others': ["top hits", "mainstream"]
    }

    # Construct the query based on the emotion
    if emotion in genre:
        query = ' OR '.join([f'genre: {g}' for g in genre[emotion]])
        try:
            results = sp.search(q=query, type='track')
        except spotipy.exceptions.SpotifyException as e:
            print(f"Spotify API error: {e}")
            
    return results['tracks']['items']

# conversation = "I feel like dancing"
# emotion = get_emotion(conversation=conversation)
# query = mood_genre_mapping(emotion=emotion)


# with open('recommended_tracks.json', 'w') as json_file:
#     json.dump(results, json_file, indent=4)
# print("Mood is", emotion)
# print("Tracks are as follows")
# pprint(results['tracks']['items'])

# tracks = results['tracks']['items']