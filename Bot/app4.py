import subprocess
import streamlit as st
import requests
import time
import os
import re
import sys

sys.path.append("/Users/omdeshmukh/Downloads/MachineLearning/Projects/Moodify")
from utils.rasa_api import send_message_to_rasa, start_rasa_action_server, start_rasa_server
from utils.display import parse_track_details, display_chat_history


# Start RASA and Action Servers
if 'rasa_process' not in st.session_state:
    st.session_state['rasa_process'] = start_rasa_server()
if 'action_process' not in st.session_state:
    st.session_state['action_process'] = start_rasa_action_server()

# Allow time for servers to start
time.sleep(20)

st.title("Moodify")

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
        

# Display chat history
display_chat_history(session_state=st.session_state)

# Gracefully shutdown servers on exit
def exit_handler():
    st.session_state['rasa_process'].terminate()
    st.session_state['action_process'].terminate()

import atexit
atexit.register(exit_handler)