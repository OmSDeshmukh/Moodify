import requests
import streamlit as st
import subprocess
from dotenv import load_dotenv
import os

load_dotenv()

def start_rasa_server():
    '''
    A function to start the rasa server for interacting with the bot
    '''
    bot_path = os.getenv('BOT_PATH')
    return subprocess.Popen(["rasa", "run", "--enable-api", "--cors", "*", "--port", "5005"], cwd=bot_path)


def start_rasa_action_server():
    '''
    A function to start the rasa action server for custom actions
    '''
    bot_path = os.getenv('BOT_PATH')
    return subprocess.Popen(["rasa", "run", "actions", "--port", "5055"], cwd=bot_path)


def send_message_to_rasa(message, sender="user"):
    '''
    Function to talk with the rasa chatbot through API
    '''
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

# def main():
#     print("Start chatting with your RASA bot (type 'exit' to stop)...")
#     while True:
#         user_message = input("You: ")
#         if user_message.lower() == 'exit':
#             break

#         responses = send_message_to_rasa(user_message)
#         if responses:
#             for response in responses:
#                 print(f"Bot: {response['text']}")

# if __name__ == "__main__":
#     main()