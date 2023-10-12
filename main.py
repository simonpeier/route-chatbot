import os

import requests
from google.cloud import dialogflow

# path to the key-file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "aifo-miniproject-401806-0b78e72e0f2f.json"
api_key = "AIzaSyCEnDQGxcTkbQVazIXFO-E081PYAvciANY"
api_url = 'https://maps.googleapis.com/maps/api/directions/json?'


# example from  https://cloud.google.com/dialogflow/es/docs/quick/api#detect-intent-text-python
def detect_intent_demo(project_id, session_id, texts, language_code):
    """
    https://cloud.google.com/dialogflow/es/docs/quick/api#detect-intent-text-python

    Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    # from google.cloud import dialogflow

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
        print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
        print(f"Origin: {response.query_result.parameters['origin']['city']}")
        print(f"Destination: {response.query_result.parameters['destination']['city']}")
        print(f"Travelmode: {response.query_result.parameters['travelmode']}")

        params = {
            'origin': response.query_result.parameters['origin']['city'],
            'destination': response.query_result.parameters['destination']['city'],
            'travel_mode': response.query_result.parameters['travelmode'],
            'key': api_key
        }

        response = requests.get(api_url, params=params)
        print(response.text)

        if response.status_code == 200:
            data = response.json()
            distance = data['routes'][0]['legs'][0]['distance']['text']
            duration = data['routes'][0]['legs'][0]['duration']['text']
            print(f"Distance: {distance}")
            print(f"Duration: {duration}")
        else:
            print(f"Request failed with status code {response.status_code}")


if __name__ == "__main__":
    # change the values accordingly
    detect_intent_demo('aifo-miniproject-401806', 'no-session-ID', ['I want to go from Winterthur to Genf by car'], 'en')
