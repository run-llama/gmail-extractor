import re
from typing import Dict, List, Any
def extract_itinerary(email_body: str) -> List[Dict[str, Any]]:
    """Extracts flight itineraries from email body.
    Returns:
        A list of dictionaries, each containing the origin and destination of a flight.
    """
    itineraries = []
    # Example: "Confirmation code: WQISDB"
    confirmation_code_match = re.search(r'Confirmation code:\s*(\w+)', email_body)
    if confirmation_code_match:
        # Example: "3:59 PM\n                        BZE\n                    Belize City, Belize"
        origin_match = re.search(r'(\d{1,2}:\d{2} [AP]M)\s+(\w{3})\s+([\w\s,]+)', email_body)
        # Example: "11:59 PM                    \n                        SFO\n                    San Francisco"
        destination_match = re.search(r'(\d{1,2}:\d{2} [AP]M)\s*\n?\s*(\w{3})\s*\n?\s*([\w\s,]+)', email_body)
        if origin_match and destination_match:
            origin_city = origin_match.group(3).strip()
            destination_city = destination_match.group(3).strip()
            itineraries.append({
                "isItinerary": True,
                "origin": origin_city,
                "destination": destination_city
            })
    # Example: <p style=3D=22color:=23222222;font-weight:bold;font-siz=\ne:18px;line-height:26px;text-align:left;=22>6:00 AM</p>
    # Example: <p style=3D=22color:=23222222;font-weight:bold;font-siz=\ne:48px;line-height:54px;text-align:left;=22>SFO</p>
    # Example: <p style=3D=22color:=23222222;font-size:18px;line-heigh=\nt:26px;text-align:left;=22>San Francisco</p>
    if not itineraries:
        origin_match = re.search(r'<p style=3D=22color:=23222222;font-weight:bold;font-siz=\
e:18px;line-height:26px;text-align:left;=22>.*?(\d{1,2}:\d{2} [AP]M)<\/p>\s*<p style=3D=22color:=23222222;font-weight:bold;font-siz=\
e:48px;line-height:54px;text-align:left;=22>(\w{3})<\/p>\s*<p style=3D=22color:=23222222;font-size:18px;line-heigh=\
t:26px;text-align:left;=22>([\w\s,]+)<\/p>', email_body, re.DOTALL)
        destination_match = re.search(r'<p style=3D=22color:=23222222;font-weight:bold;font-siz=\
e:18px;line-height:26px;text-align:right;=22>.*?(\d{1,2}:\d{2} [AP]M)<\/p>\s*<p style=3D=22color:=23222222;font-weight:bold;font-siz=\
e:48px;line-height:54px;text-align:right;=22>(\w{3})<\/p>\s*<p style=3D=22color:=23222222;font-size:18px;line-heigh=\
t:26px;text-align:right;=22>([\w\s,]+)<\/p>', email_body, re.DOTALL)
        if origin_match and destination_match:
            origin_city = origin_match.group(3).strip()
            destination_city = destination_match.group(3).strip()
            itineraries.append({
                "isItinerary": True,
                "origin": origin_city,
                "destination": destination_city
            })
    # TripIt itinerary
    if not itineraries:
        origin_match = re.search(r'your trip to ([\w\s,]+) starts', email_body)
        if origin_match:
            origin_city = origin_match.group(1).strip()
            itineraries.append({
                "isItinerary": True,
                "origin": origin_city,
                "destination": origin_city  # TripIt doesn't include the destination in this email
            })
    # Alaska Airlines Itinerary
    if not itineraries:
        origin_match = re.search(r'\*\s*(Sun|Mon|Tue|Wed|Thu|Fri|Sat), (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2} \d{1,2}:\d{2} [AP]M \*\n\* (\w{3}) \*\n([\w\s,]+)', email_body)
        destination_match = re.search(r'\*\s*(Sun|Mon|Tue|Wed|Thu|Fri|Sat), (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2} \d{1,2}:\d{2} [AP]M \*\n\* (\w{3}) \*\n([\w\s,]+)', email_body)
        if origin_match and destination_match:
            origin_city = origin_match.group(4).strip()
            destination_city = destination_match.group(4).strip()
            itineraries.append({
                "isItinerary": True,
                "origin": origin_city,
                "destination": destination_city
            })
    # JetBlue Itinerary
    if not itineraries:
        origin_match = re.search(r'mi_origin=3D(\w{3})', email_body)
        destination_match = re.search(r'mi_destination=3D(\w{3})', email_body)
        if origin_match and destination_match:
            origin_city = origin_match.group(1).strip()
            destination_city = destination_match.group(1).strip()
            itineraries.append({
                "isItinerary": True,
                "origin": origin_city,
                "destination": destination_city
            })
    # Alaska Airlines Itinerary - alternate format
    if not itineraries:
        origin_match = re.search(r'Confirmation code:\n\*(\w+)\*<\/a>\n\n\n\*Alaska\*\nFlight \d+\n.*?\n\*\s*(Sun|Mon|Tue|Wed|Thu|Fri|Sat), (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2} \d{1,2}:\d{2} [AP]M \*\n\* (\w{3}) \*\n([\w\s,]+)\n', email_body)
        destination_match = re.search(r'Confirmation code:\n\*(\w+)\*<\/a>\n\n\n\*Alaska\*\nFlight \d+\n.*?\n\*\s*(Sun|Mon|Tue|Wed|Thu|Fri|Sat), (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2} \d{1,2}:\d{2} [AP]M \*\n\* (\w{3}) \*\n([\w\s,]+)\n.*?\n\*\s*(Sun|Mon|Tue|Wed|Thu|Fri|Sat), (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2} \d{1,2}:\d{2} [AP]M \*\n\* (\w{3}) \*\n([\w\s,]+)\n', email_body)
        if origin_match and destination_match:
            origin_city = origin_match.group(5).strip()
            destination_city = destination_match.group(8).strip()
            itineraries.append({
                "isItinerary": True,
                "origin": origin_city,
                "destination": destination_city
            })
    return itineraries
