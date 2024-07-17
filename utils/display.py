import re
import streamlit as st


def display_chat_history(session_state):
    '''
    Function to display chats along with history in the Streamlit UI
    '''
    st.markdown(
        """
        <style>
        .user-msg {
            background-color: #dcf8c6;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            text-align: right;
        }
        .bot-msg {
            background-color: #f1f0f0;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            text-align: left;
        }
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
    
    for chat in session_state['chat_history']:
        if chat['sender'] == 'user':
            st.markdown(f"<div class='user-msg'>{chat['message']}</div>", unsafe_allow_html=True)
        else:
            if chat.get('type') == 'track':
                preview_url = chat.get('preview_url')
                preview_link = f"<a href='{preview_url}' class='track-link' target='_blank'>Listen to Preview</a>" if preview_url else ""
                st.markdown(
                    f"""
                    <div class='track-container'>
                        <div class='track-title'>{chat['title']}</div>
                        <div class='track-details'><strong>Artist:</strong> {chat['artist']}</div>
                        <div class='track-details'><strong>Album:</strong> {chat['album']}</div>
                        <div class='track-details'><strong>Duration:</strong> {chat['duration']}</div>
                        {preview_link}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(f"<div class='bot-msg'>{chat['message']}</div>", unsafe_allow_html=True)
                
    return


def parse_track_details(text):
    '''
    Function to parse the track details returned by the Spotify API
    '''
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
