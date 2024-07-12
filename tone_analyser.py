from pysentimiento import create_analyzer
import transformers
import numpy as np

device='mps'
transformers.logging.set_verbosity(transformers.logging.ERROR)
emotion_analyzer = create_analyzer(task="emotion", lang="en")


def get_emotion(conversation):
    '''
    Function to get emotions from a conversation
    '''
    emotion_scores = emotion_analyzer.predict(conversation).probas
    keys = list(emotion_scores.keys())
    values = list(emotion_scores.values())
    sorted_value_index = np.argsort(values)
    sorted_value_index = sorted_value_index[::-1]
    sorted_dict = {keys[i]: values[i] for i in sorted_value_index}
    del sorted_dict['others']
    print(sorted_dict)
    
get_emotion("i am not very angry")