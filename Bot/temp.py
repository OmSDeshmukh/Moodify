from rasa.core.agent import Agent
from rasa.core.interpreter import NaturalLanguageInterpreter
from rasa.core.utils import EndpointConfig
from rasa.core.tracker_store import InMemoryTrackerStore

# Initialize interpreter (NLU)
interpreter = NaturalLanguageInterpreter.create("path/to/nlu_model")

# Configure endpoints for action server
action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")

# Initialize tracker store (optional)
tracker_store = InMemoryTrackerStore(domain=None)

# Initialize agent
agent = Agent.load("path/to/core_model", interpreter=interpreter, action_endpoint=action_endpoint, tracker_store=tracker_store)

# Example interaction
while True:
    user_input = input("You: ")
    if user_input.lower() == '/stop':
        break
    
    # Get response from Rasa agent
    responses = agent.handle_text(user_input)
    for response in responses:
        print(f"Bot: {response['text']}")