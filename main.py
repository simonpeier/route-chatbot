import os

import requests
from google.cloud import dialogflow

# path to the key-file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "aifo-miniproject-401806-0b78e72e0f2f.json"
api_key = "AIzaSyCEnDQGxcTkbQVazIXFO-E081PYAvciANY"
api_url = 'https://maps.googleapis.com/maps/api/directions/json?'


# example from  https://cloud.google.com/dialogflow/es/docs/quick/api#detect-intent-text-python
def detect_intent(project_id, session_id, texts, language_code):
    """
    https://cloud.google.com/dialogflow/es/docs/quick/api#detect-intent-text-python

    Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence
            )
        )

        origin = response.query_result.parameters['origin']['city']
        destination = response.query_result.parameters['destination']['city']
        travelmode = response.query_result.parameters['travelmode']

        print_dialogflow_query_parameters(destination, origin, response, travelmode)

        fetch_route(destination, origin, travelmode)


def fetch_route(destination, origin, travelmode):
    params = {
        'origin': origin,
        'destination': destination,
        'mode': travelmode.lower(),
        'key': api_key
    }
    response = requests.get(api_url, params=params)
    print(f"Directions api url: {response.url}\n")

    if response.status_code == 200:
        routes = response.json()['routes']
        if not routes:
            print("Could not find origin or destination, please be more specific")
        else:
            distance = routes[0]['legs'][0]['distance']['text']
            duration = routes[0]['legs'][0]['duration']['text']
            print(f"Distance: {distance}")
            print(f"Duration: {duration}")
    else:
        print(f"Request failed with status code {response.status_code}")


def print_dialogflow_query_parameters(destination, origin, response, travelmode):
    print("Fulfillment text: {}".format(response.query_result.fulfillment_text))
    print(f"Origin: {origin}")
    print(f"Destination: {destination}")
    print(f"Travelmode: {travelmode}\n")


if __name__ == "__main__":
    # change the values accordingly
    detect_intent('aifo-miniproject-401806', 'no-session-ID', ['I want to go from Geneva to Zürich by transit'], 'en')
