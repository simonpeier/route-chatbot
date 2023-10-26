import requests

api_key = "AIzaSyCEnDQGxcTkbQVazIXFO-E081PYAvciANY"
directions_url = 'https://maps.googleapis.com/maps/api/directions/json?'
places_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'


def fetch_route(destination, origin, travelmode):
    params = {
        'origin': origin,
        'destination': destination,
        'mode': travelmode,
        'key': api_key
    }
    response = requests.get(directions_url, params=params)

    if response.status_code == 200:
        routes = response.json()['routes']
        if not routes:
            return "Could not find origin or destination, please be more specific"
        else:
            distance = routes[0]['legs'][0]['distance']['text']
            duration = routes[0]['legs'][0]['duration']['text']
            return f"Distance: {distance} \nDuration: {duration}\n"
    else:
        return f"Request failed with status code {response.status_code}"


def fetch_places(city, placetype):
    params = {
        'query': city,
        'type': placetype,
        'key': api_key
    }
    response = requests.get(places_url, params=params)

    if response.status_code == 200:
        results = response.json()['results']
        if not results:
            return f"Looks like there is no {placetype} in {city}"
        else:
            if len(results) < 3:
                name = results[0]['name']
                address = results[0]['formatted_address']
                return f"Name: {name} \nAddress: {address}\n"
            else:
                top_results = ""
                for id_entries in range(3):
                    name = results[id_entries]['name']
                    address = results[id_entries]['formatted_address']
                    top_results = top_results + f"Name: {name}\nAddress: {address}\n\n"
                return top_results
    else:
        return f"Request failed with status code {response.status_code}"
