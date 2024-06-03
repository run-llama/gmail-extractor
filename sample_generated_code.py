import re
from typing import Dict, List, Any

def extract_itinerary_details(email_body: str) -> List[Dict[str, Any]]:
    """Extracts itinerary details from an email body.

    Args:
        email_body: The email body text.

    Returns:
        A list of dictionaries, where each dictionary represents an itinerary
        and contains the following keys:
            - isItinerary: True if the email is an itinerary, False otherwise
            - origin: The origin of the flight
            - destination: The destination of the flight
    """
    itineraries = []

    # Example: Extract origin and destination from Alaska Airlines email
    if 'alaskaair' in email_body.lower():
        match = re.search(r'from ([A-Z]+).* to ([A-Z]+)', email_body)
        if match:
            origin = match.group(1)
            destination = match.group(2)
            itineraries.append({
                "isItinerary": True,
                "origin": origin,
                "destination": destination
            })

    # Extract origin and destination from Alaska Airlines email
    if 'Confirmation code' in email_body:
        match = re.search(r'(\d{2}:\d{2} [AP]M)\s+([A-Z]+)\s+<br />\s+([A-Za-z]+, [A-Za-z]+)\s+<br />.*\d{2}:\d{2} [AP]M\s+([A-Z]+)\s+<br />\s+([A-Za-z]+, [A-Za-z]+)', email_body)
        if match:
            origin = match.group(2) + ', ' + match.group(3)
            destination = match.group(4) + ', ' + match.group(5)
            itineraries.append({
                "isItinerary": True,
                "origin": origin,
                "destination": destination
            })

    # Extract origin and destination from JetBlue email
    if 'Prices shown:' in email_body:
        match = re.search(r'Prices shown: ([A-Z]+) to ([A-Z]+)\.', email_body)
        if match:
            origin = match.group(1)
            destination = match.group(2)
            itineraries.append({
                "isItinerary": True,
                "origin": origin,
                "destination": destination
            })

    # Extract origin and destination from this Alaska Airlines email
    if 'Your confirmation receipt:' in email_body:
        match = re.search(r'\* ([A-Z]{3}) \*.*\* ([A-Z]{3}) \*', email_body)
        if match:
            origin = match.group(1)
            destination = match.group(2)
            itineraries.append({
                "isItinerary": True,
                "origin": origin,
                "destination": destination
            })
    # Extract origin and destination from this Alaska Airlines email
    if 'Alaska\nFlight' in email_body:
        match = re.search(r'06:00 AM\n([A-Z]{3}).*\n.*\n02:49 PM\n([A-Z]{3})', email_body)
        if match:
            origin = match.group(1)
            destination = match.group(2)
            itineraries.append({
                "isItinerary": True,
                "origin": origin,
                "destination": destination
            })
    # Extract origin and destination from this JetBlue email
    if 'Your flight from' in email_body:
        match = re.search(r'Your flight from ([A-Za-z]+) departs.*\.', email_body)
        if match:
            origin = match.group(1)
            match = re.search(r'Check in for your flight to ([A-Za-z ]+)\.', email_body)
            if match:
                destination = match.group(1)
                itineraries.append({
                    "isItinerary": True,
                    "origin": origin,
                    "destination": destination
                })
    # Extract origin and destination from this JetBlue email
    if 'Your JetBlue confirmation code is' in email_body:
        match = re.search(r'nowrap style=3D=22font-family: Arial,sans-serif;font-size:16px;padding-bottom:10px;color:=23000064=22>\n                                    ([A-Z]{3}) &nbsp;\n                                    <img src=3D=22https://email=2Ejetblue=2Ecom/assets/responsysimages/content/jetblue/JB_PreTrip_GreenArrow=2Epng=22 width=3D=2212=22 style=3D=22font-family: Arial, sans-serif;  margin: 0 auto; padding: 0;width:12px;=22 border=3D=220=22 alt=3D=22=22/>\n                                    &nbsp;=20\n                                    <span style=3D=22color:=23000064;font-size:16px;font-family: Arial, sans-serif;=22>([A-Z]{3})</span>', email_body)
        if match:
            origin = match.group(1)
            destination = match.group(2)
            itineraries.append({
                "isItinerary": True,
                "origin": origin,
                "destination": destination
            })
    # Extract origin and destination from this JetBlue email
    if 'Check in for your flight to' in email_body:
        match = re.search(r'Your flight from ([A-Za-z]+) departs.*\.', email_body)
        if match:
            origin = match.group(1)
        match = re.search(r'Check in for your flight to ([A-Za-z]+)\.', email_body)
        if match:
            destination = match.group(1)
            itineraries.append({
                "isItinerary": True,
                "origin": origin,
                "destination": destination
            })
    # Extract origin and destination from this JetBlue email
    if 'Your Flight Itinerary' in email_body:
        match = re.search(r'nowrap style=3D=22font-family: Arial,sans-serif;font-size:16px;padding-bottom:10px;color:=23000064=22>\n                                    ([A-Z]{3}) &nbsp;\n                                    <img src=3D=22https://email=2Ejetblue=2Ecom/assets/responsysimages/content/jetblue/JB_PreTrip_GreenArrow=2Epng=22 width=3D=2212=22 style=3D=22font-family: Arial, sans-serif;  margin: 0 auto; padding: 0;width:12px;=22 border=3D=220=22 alt=3D=22=22/>\n                                    &nbsp;=20\n                                    <span style=3D=22color:=23000064;font-size:16px;font-family: Arial, sans-serif;=22>([A-Z]{3})</span>', email_body)
        if match:
            origin = match.group(1)
            destination = match.group(2)
            itineraries.append({
                "isItinerary": True,
                "origin": origin,
                "destination": destination
            })
    # Extract origin and destination from this JetBlue email
    if 'mi_origin=' in email_body:
        match = re.search(r'mi_origin=3D([A-Z]{3})&', email_body)
        if match:
            origin = match.group(1)
        match = re.search(r'mi_destination=3D([A-Z]{3})&', email_body)
        if match:
            destination = match.group(2)
            itineraries.append({
                "isItinerary": True,
                "origin": origin,
                "destination": destination
            })
    # Extract origin and destination from this JetBlue email
    if 'Just want flights? Put added value on the itinerary with our everyday low fares' in email_body:
        match = re.search(r'mi_origin=3D([A-Z]{3})&', email_body)
        if match:
            origin = match.group(1)
        match = re.search(r'mi_destination=3D([A-Z]{3})&', email_body)
        if match:
            destination = match.group(2)
            itineraries.append({
                "isItinerary": True,
                "origin": origin,
                "destination": destination
            })
    # Extract origin and destination from this Hawaiian Airlines email
    if 'font-size:11pt;scrolling:no;" ><b >OAKLAND</b>' in email_body:
        match = re.search(r'font-size:11pt;scrolling:no;" ><b >([A-Za-z]+)</b>.*font-size:11pt;scrolling:no;" ><b >([A-Za-z]+)</b>', email_body)
        if match:
            origin = match.group(1)
            destination = match.group(2)
            itineraries.append({
                "isItinerary": True,
                "origin": origin,
                "destination": destination
            })
    # Extract origin and destination from this TripIt email
    if 'your trip to' in email_body:
        match = re.search(r'your trip to (.*?) starts', email_body)
        if match:
            destination = match.group(1)
            itineraries.append({
                "isItinerary": True,
                "origin": None,
                "destination": destination
            })

    return itineraries
