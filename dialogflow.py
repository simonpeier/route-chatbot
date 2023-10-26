import os
import re

from google.cloud import dialogflow

from google_api_fetch import fetch_route, fetch_places

# path to the key-file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "aifo-miniproject-401806-0b78e72e0f2f.json"


def detect_intent(text):
    project_id = 'aifo-miniproject-401806'
    session_id = 'no-session-ID'
    language_code = 'en'

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    fulfillment_text = re.sub(r'\s+', ' ', response.query_result.fulfillment_text)
    print(f"INTENT: {response.query_result.intent.display_name}")
    print(f"PARAMETERS: {fulfillment_text}\n")

    if not fulfillment_text.startswith("#"):
        return [fulfillment_text]
    else:
        dialogflow_text = fulfillment_text[1:]
        question_text = "Do you need something else?"
        if response.query_result.intent.display_name == "request.route - yes":
            for context in response.query_result.output_contexts:
                if context.name.endswith("requestroute-followup"):
                    origin = context.parameters.get("origin")["city"]
                    destination = context.parameters.get("destination")["city"]
                    travelmode = context.parameters.get("travelmode")
                    print_route_parameters(destination, origin, travelmode)
                    message = f"{dialogflow_text}\n\n{fetch_route(destination, origin, travelmode)}"
                    return [message, question_text]
        elif response.query_result.intent.display_name == "find.place - yes":
            for context in response.query_result.output_contexts:
                if context.name.endswith("findplace-followup"):
                    city = context.parameters.get("location")["city"]
                    placetype = context.parameters.get("placetype")
                    print_place_parameters(city, placetype)
                    message = f"{dialogflow_text}\n\n{fetch_places(city, placetype)}"
                    return [message, question_text]


def print_route_parameters(destination, origin, travelmode):
    print(f"Origin:  {origin}")
    print(f"Destination: {destination}")
    print(f"Travelmode: {travelmode}\n")


def print_place_parameters(location, placetype):
    print(f"Location: {location}")
    print(f"Type: {placetype}\n")
