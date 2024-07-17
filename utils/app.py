import streamlit as st
import json
import random

from utils.songs import mood_genre_mapping
from utils.tone_analyser import get_emotion


# Function to display recommendations
def display_recommendations(tracks):
    for track in tracks:
        song_name = track['name']
        artist_name = ", ".join([artist['name'] for artist in track['artists']])
        album_name = track['album']['name']
        preview_url = track['preview_url']
        duration_ms = track['duration_ms']
        duration_min = duration_ms // 60000
        duration_sec = (duration_ms % 60000) // 1000

        st.markdown(f"### {song_name}")
        st.markdown(f"**Artist:** {artist_name}")
        st.markdown(f"**Album:** {album_name}")
        st.markdown(f"**Duration:** {duration_min} min {duration_sec} sec")
        if preview_url:
            st.markdown(f"[Listen to Preview]({preview_url})")
        else:
            st.markdown("Preview not available")
        st.markdown("---")

# Streamlit UI
st.title("Music Recommendation Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "recommendations" not in st.session_state:
    st.session_state.recommendations = []

user_input = st.text_input("You: ", "")

if user_input:
    st.session_state.chat_history.append(f"You: {user_input}")
    tone = get_emotion(user_input)
    st.session_state.chat_history.append(f"Bot: It seems like you're feeling {tone}")

    recommended_tracks = mood_genre_mapping(tone)
    st.session_state.recommendations = recommended_tracks

st.markdown("## Chat History")
for message in st.session_state.chat_history:
    st.write(message)

st.markdown("---")

st.markdown("## Recommendations")
display_recommendations(st.session_state.recommendations)