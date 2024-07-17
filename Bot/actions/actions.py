# actions/actions.py
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import sys 

sys.path.append("/Users/omdeshmukh/Downloads/MachineLearning/Projects/Moodify")
from utils.songs import get_tracks
from utils.tone_analyser import get_emotion

global tracks
tracks = []

# Class to keep track of tones of the user and fetch relative music
class ActionAnalyseTone(Action):
    def __init__(self) -> None:
        super().__init__()
        self.analyze_tone = get_emotion
        self.get_songs = get_tracks
        
    def name(self) -> str:
        return "action_analyze_tone_and_fetch_music"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        user_message = tracker.latest_message.get('text')
        mood = self.analyze_tone(conversation=user_message)
        
        # Correctly set the slot value
        events = [SlotSet("mood", mood)]
        
        track = self.get_songs(mood)
        tracks.append(track)
        # response = "Here are some tracks for your mood:\n" + "\n".join(tracks)
        
        # dispatcher.utter_message(text=response)
        return events
    
    
# Class to recommend songs to the user
class ActionRecommendTracks(Action):
    def name(self) -> str:
        return "action_recommend_tracks"

    def run(self, dispatcher: CollectingDispatcher,
            tracker,
            domain) -> list:
        # Display recommendations using display_recommendations function
        self.display_recommendations(tracks, dispatcher)

        return []

    def display_recommendations(self, tracks, dispatcher: CollectingDispatcher):
        if not tracks:
            dispatcher.utter_message(text="No tracks found for this mood.")
            return

        for track_list in tracks:
            for track in track_list:
                song_name = track['name']
                artist_name = ", ".join([artist['name'] for artist in track['artists']])
                album_name = track['album']['name']
                preview_url = track['preview_url']
                duration_ms = track['duration_ms']
                duration_min = duration_ms // 60000
                duration_sec = (duration_ms % 60000) // 1000

                response = f"### {song_name}\n" \
                           f"**Artist:** {artist_name}\n" \
                           f"**Album:** {album_name}\n" \
                           f"**Duration:** {duration_min} min {duration_sec} sec\n"

                if preview_url:
                    response += f"[Listen to Preview]({preview_url})\n"
                else:
                    response += "Preview not available\n"

                response += "---"
                dispatcher.utter_message(text=response)
    
    
# class MockTracker:
#     def __init__(self, sender_id, slots=None, latest_message=None):
#         self.sender_id = sender_id
#         self.slots = slots if slots else {}
#         self.latest_message = latest_message if latest_message else {}

#     def get_slot(self, slot_name):
#         return self.slots.get(slot_name)

#     def set_slot(self, slot_name, value):
#         self.slots[slot_name] = value

#     def get_latest_message(self):
#         return self.latest_message

# # Example usage to test ActionAnalyseTone
# tracker = MockTracker(
#     sender_id="test_user",
#     latest_message={"text": "I'm feeling happy"}
# )
# dispatcher = CollectingDispatcher()

# action_analyse_tone = ActionAnalyseTone()
# events = action_analyse_tone.run(dispatcher=dispatcher, tracker=tracker, domain={})
# # print(tracks)  # Check tracks list after running the action

# # Example usage to test ActionRecommendTracks
# tracker = MockTracker(
#     sender_id="test_user",
#     slots={"mood": "happy"}  # Set mood slot
# )

# action_recommend_tracks = ActionRecommendTracks()
# response_events = action_recommend_tracks.run(dispatcher=dispatcher, tracker=tracker, domain={})
# print(response_events)  # Check the response events