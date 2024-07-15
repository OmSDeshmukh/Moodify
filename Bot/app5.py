import subprocess
import streamlit as st
from streamlit_chat import message
import requests
import time
import re

# Bot using the streamchat
def start_rasa_server():
    return subprocess.Popen(["rasa", "run", "--enable-api", "--cors", "*", "--port", "5005"])

def start_rasa_action_server():
    return subprocess.Popen(["rasa", "run", "actions", "--port", "5055"])

def send_message_to_rasa(message, sender="user"):
    url = "http://localhost:5005/webhooks/rest/webhook"
    payload = {
        "sender": sender,
        "message": message
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to send message. Status code: {response.status_code}")
        st.error(response.text)
        return None

def parse_track_details(text):
    track_info = {}
    
    title_match = re.search(r'###\s*(.+)', text)
    artist_match = re.search(r'\*\*Artist:\*\*\s*(.+)', text)
    album_match = re.search(r'\*\*Album:\*\*\s*(.+)', text)
    duration_match = re.search(r'\*\*Duration:\*\*\s*(.+)', text)
    preview_match = re.search(r'\[Listen to Preview\]\((.+)\)', text)
    
    if title_match:
        track_info['title'] = title_match.group(1)
    if artist_match:
        track_info['artist'] = artist_match.group(1)
    if album_match:
        track_info['album'] = album_match.group(1)
    if duration_match:
        track_info['duration'] = duration_match.group(1)
    if preview_match:
        track_info['preview_url'] = preview_match.group(1)
    
    return track_info

# Start RASA and Action Servers if not already started
if 'rasa_process' not in st.session_state:
    st.session_state['rasa_process'] = start_rasa_server()
if 'action_process' not in st.session_state:
    st.session_state['action_process'] = start_rasa_action_server()

# Allow time for servers to start
time.sleep(10)

st.title("Chat with RASA Bot")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input area for user message
user_message = st.text_input("You:", key="user_message_input")

if st.button("Send"):
    if user_message:
        # Append user message to chat history
        st.session_state['chat_history'].append({"sender": "user", "message": user_message})
        
        # Send message to RASA bot
        responses = send_message_to_rasa(user_message)
        
        # Append bot responses to chat history
        if responses:
            for response in responses:
                if 'Artist' in response['text'] and 'Album' in response['text'] and 'Duration' in response['text']:
                    track_info = parse_track_details(response['text'])
                    track_info['sender'] = 'bot'
                    track_info['type'] = 'track'
                    st.session_state['chat_history'].append(track_info)
                else:
                    st.session_state['chat_history'].append({"sender": "bot", "message": response['text']})
        
        # # Clear the input field by setting the widget's key to an empty string
        # st.session_state['user_message_input'] = ""

# Custom CSS for the track container
st.markdown(
    """
    <style>
    .track-container {
        border: 1px solid #ddd;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 10px;
    }
    .track-title {
        font-size: 1.2em;
        font-weight: bold;
    }
    .track-details {
        margin: 5px 0;
    }
    .track-link {
        color: #1DB954;
        text-decoration: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display chat history
for i, chat in enumerate(st.session_state['chat_history']):
    if chat['sender'] == 'user':
        message(chat['message'], is_user=True, key=f"user_{i}")
    else:
        if chat.get('type') == 'track':
            track_info = f"""
            Title: {chat['title']}\n
            Artist: {chat['artist']}\n
            Album: {chat['album']}\n
            Duration: {chat['duration']}\n
            [Listen to Preview]({chat['preview_url']})
            """
            message(track_info, key=f"bot_{i}")
        else:
            message(chat['message'], key=f"bot_{i}")

# Gracefully shutdown servers on exit
def exit_handler():
    st.session_state['rasa_process'].terminate()
    st.session_state['action_process'].terminate()

import atexit
atexit.register(exit_handler)