import os

import requests
from google.cloud import dialogflow

# path to the key-file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "aifo-miniproject-401806-0b78e72e0f2f.json"
api_key = "AIzaSyCEnDQGxcTkbQVazIXFO-E081PYAvciANY"
directions_url = 'https://maps.googleapis.com/maps/api/directions/json?'
places_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'


def detect_intent(texts):
    project_id = 'aifo-miniproject-401806'
    session_id = 'no-session-ID'
    language_code = 'en'

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    # print("Session path: {}\n".format(session))

    for text in texts:
        while True:
            text_input = dialogflow.TextInput(text=text, language_code=language_code)

            query_input = dialogflow.QueryInput(text=text_input)

            response = session_client.detect_intent(
                request={"session": session, "query_input": query_input}
            )

            if response.query_result.intent.display_name == "Default Fallback Intent":
                text = input(response.query_result.fulfillment_text + "\n")
            elif response.query_result.fulfillment_text != "completed":
                text = input(response.query_result.fulfillment_text + "\n")
            else:
                # print(response.query_result.fulfillment_text + "\n")
                # print("=" * 20)
                # print("Query text: {}".format(response.query_result.query_text))
                # print(
                #     "Detected intent: {} (confidence: {})\n".format(
                #         response.query_result.intent.display_name,
                #         response.query_result.intent_detection_confidence
                #     )
                # )

                if response.query_result.intent.display_name == "request.route":
                    origin = response.query_result.parameters['origin']['city']
                    destination = response.query_result.parameters['destination']['city']
                    travelmode = response.query_result.parameters['travelmode']
                    print_dialogflow_query_parameters(destination, origin, response, travelmode)
                    fetch_route(destination, origin, travelmode)
                    break
                elif response.query_result.intent.display_name == "find.place":
                    location = response.query_result.parameters['location']['city']
                    type = response.query_result.parameters['placetype']
                    print(f"Location: {location}")
                    print(f"Type: {type}\n")
                    fetch_places(location, type)
                    break


def fetch_route(destination, origin, travelmode):
    params = {
        'origin': origin,
        'destination': destination,
        'mode': travelmode,
        'key': api_key
    }
    response = requests.get(directions_url, params=params)
    # print(f"Directions api url: {response.url}\n")

    if response.status_code == 200:
        routes = response.json()['routes']
        if not routes:
            print("Could not find origin or destination, please be more specific")
        else:
            distance = routes[0]['legs'][0]['distance']['text']
            duration = routes[0]['legs'][0]['duration']['text']
            print(f"Distance: {distance}")
            print(f"Duration: {duration}\n")
    else:
        print(f"Request failed with status code {response.status_code}")


def fetch_places(location, type):
    params = {
        'query': location,
        'type': type,
        'key': api_key
    }
    response = requests.get(places_url, params=params)
    # print(f"Directions api url: {response.url}\n")

    if response.status_code == 200:
        results = response.json()['results']
        if not results:
            print(f"Looks like there is no {type} in {location}")
        else:
            if len(results) < 3:
                name = results[0]['name']
                address = results[0]['formatted_address']
                print(f"Name: {name}")
                print(f"Address: {address}\n")
            else:
                for id_entries in range(3):
                    name = results[id_entries]['name']
                    address = results[id_entries]['formatted_address']
                    print(f"Name: {name}")
                    print(f"Address: {address}\n")
                    print("=" * 20 + "\n")
    else:
        print(f"Request failed with status code {response.status_code}")


def print_dialogflow_query_parameters(destination, origin, response, travelmode):
    # print("Fulfillment text: {}".format(response.query_result.fulfillment_text))
    print(f"Origin: {origin}")
    print(f"Destination: {destination}")
    print(f"Travelmode: {travelmode}\n")


if __name__ == "__main__":
    while True:
        user_input = input("How can I help you? \n")
        detect_intent([user_input])
        another_route = input("Do you need something else? (y/n)\n")
        if another_route.lower() == "y":
            continue
        else:
            break
