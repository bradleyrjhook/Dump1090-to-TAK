# DUMP1090-TO-TAK
# VER 1.1a

import time
import socket
import requests
import os
import json
import urllib.parse

UDP_IP = "255.255.255.255"  # Broadcast address
UDP_PORT = 6969
POLL_INTERVAL = 3  # Polling interval in seconds
DUMP1090_URL = "http://localhost:8080/data/aircraft.json"
#DUMP1090_URL = "file:///home/dump1090/dump1090-json/aircraft.json"

mil_icao_database = {
    "CAN A310": {
        "a-f-A-M-F-C": [
            "C2B355", "C2B35F", "C2B3B9", "C2B3C3", "C2B37D"
        ]
    },
    "CAN A4": {
        "a-f-A-M-F-T": [
            "C01266", "C01267", "C0126A", "C0126B", "C01271", "C01275"
        ]
    },
    "CAN AJET": {
        "a-f-A-M-F": [
            "C01479", "C026E7", "C03177", "C04BDF", "C053D9", "C0566F", "C05E5B", "C063B1",
            "C068EB", "C070D7", "C07B67", "C07B75", "C08605", "C088A9"
        ]
    },
    "CAN DH8": {
        "a-f-A-M-F-C-L": [
            "C2B2D3", "C2B2DD", "C2B2E7", "C2B2F1", "C06F16", "C2B2D3", "C2B2DD", "C2B2E7",
            "C05E11", "C07B3F", "C06DC8"
        ]
    },
    "CAN B350": {
        "a-f-A-M-F-C-L": [
            "C06820"
        ]
    },
    "CAN B350": {
        "a-f-A-M-F-C-L": [
            "C048B6"
        ]
    },
    "CAN CC144": {
        "a-f-A-M-F-C-L": [
            "C2C1F1", "C2A01B", "C2B391", "C2A000", "C2A01B", "C2B39B", "C2B3A5", "C2B3AF",
            "C2B369", "C2B373", "C06F13", "C07B39"
        ]
    },
    "CAN BALL": {
        "a-f-A-M-L": [
            "C2AEB0", "C2AEB1"
        ]
    },
    "CAN TEX2": {
        "a-f-A-M-F-T": [
            "C2AFD1", "C2AFE5", "C2AFEF", "C2AFF9", "C2B003", "C2B00D", "C2B021", "C2B02B",
            "C2B035", "C2B03F", "C2B049", "C2B053", "C2B05D", "C2B067", "C2B071", "C2B07B",
            "C2B085", "C2B08F", "C2B099", "C2B0A3", "C2B0AD", "C2B0B7", "C2B0C1", "C2B0CB",
        ]
    },
    "CAN C130": {
        "a-f-A-M-F-C-M": [
            "C2AF4F", "C2AF59", "C2AF63", "C2AF6D", "C2AF77", "C2AF81", "C2AF8B", "C2AF27",
            "C2AF95", "C2AF9F", "C2AFB3", "C2AFBD", "C2B52B", "C2B535", "C2B53F", "C2B549",
            "C2B553", "C2B55D", "C2B567", "C2B571", "C2B57B", "C2B585", "C2B58F", "C2B599",
            "C2B5A3", "C2B5AD", "C2B5B7", "C2B5C1", "C2B5CB"
        ]
    },
    "CAN C17": {
        "a-f-A-M-F-C-H": [
            "C2B3D7", "C2AFC7", "C2B3EB", "C2B3F5", "C2B3FF"
        ]
    },
    "CAN CP140": {
        "a-f-A-M-F-P": [
            "C2B1A7", "C2B1B1", "C2B1BB", "C2B1C5", "C2B1CF", "C2B1D9", "C2B1E3", "C2B1ED",
            "C2B1F7", "C2B201", "C2B20B", "C2B215", "C2B21F", "C2B229", "C2B233", "C2B23D",
            "C2B247", "C2B251" ,"C2B25B" ,"C2B265"
        ]
    },
    "CAN G120": {
        "a-f-A-M-F-T": [
            "C02820", "C02825", "C02828", "C02829", "C0282A", "C0282B", "C0282C", "C0282D",
            "C02833", "C02834", "C02835", "C06CCB", "C06CE0"
        ]
    },
    "CAN CH147": {
        "a-f-A-M-H-C-H": [
            "C2BB25", "C2BB2F", "C2BB39", "C2BB43", "C2BB4D", "C2BB57", "C2BB61", "C2BB6B",
            "C2BB75", "C2BB7F", "C2BB89", "C2BB93", "C2BB9D", "C2BBA7" , "C2BBB1"
        ]
    },
    "CAN CH148": {
        "a-f-A-M-H-S": [
            "C2B517", "C2B50D", "C2B427", "C2B459", "C2B463", "C2B46D", "C2B477", "C2B481",
            "C2B497", "C2B49F", "C2B4A9", "C2B4B3", "C2B4BD", "C2B4C7", "C2B4DB", "C2B4EF",
            "C2B4F9", "C2B503"
        ]
    },
    # Add more aircraft types as needed
}

mil_country_prefixes = {
    "United States": {"prefixes": ["AE", "AD"], "cot_type": "a-f-A-M-F"},
    "Canada": {"prefixes": ["C2"], "cot_type": "a-f-A-M-F"},
    "United Kingdom": {"prefixes": ["43"], "cot_type": "a-f-A-M-F"},
    "Australia": {"prefixes": ["7C"], "cot_type": "a-f-A-M-F"},
    "Germany": {"prefixes": ["3E", "3F"], "cot_type": "a-f-A-M-F"},
    "France": {"prefixes": ["3A", "3B"], "cot_type": "a-f-A-M-F"},
    "Italy": {"prefixes": ["33"], "cot_type": "a-f-A-M-F"},
    # Add more country prefixes and cot types as needed
}

def get_aircraft_data():
    url_parts = urllib.parse.urlparse(DUMP1090_URL)
    if url_parts.scheme == "http" or url_parts.scheme == "https":
        response = requests.get(DUMP1090_URL)
        if response.status_code == 200:
            return response.json().get("aircraft", [])
    elif url_parts.scheme == "file":
        file_path = urllib.parse.unquote(url_parts.path)
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                return data.get("aircraft", [])
        except FileNotFoundError:
            print("Aircraft data file not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON data.")
    else:
        print("Invalid URL scheme. Only HTTP and file schemes are supported.")
    return []

def feet_to_meters(feet):
    return round(feet * 0.3048, 2)

def generate_cot_message(icao, callsign, squawk, lat, lon, alt, heading):
    cot = "<event version=\"2.0\" uid=\"icao24-"
    cot += str(icao)
    cot += "\" type=\""
    
    cot_type = ""
    country = ""
    
    # Determine the country based on the ICAO prefix
    for country_prefix, info in mil_country_prefixes.items():
        prefixes = info["prefixes"]
        cot_type = info["cot_type"]
        for prefix in prefixes:
            if icao.startswith(prefix):
                country = country_prefix
                break
    
    # If the country is not found, default to civilian type
    if not country:
        cot_type = "a-n-A-C-F"
    
    cot += cot_type
    
    cot += "\" how=\"m-g\" time=\""
    cot += time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    cot += "\" start=\""
    cot += time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    cot += "\" stale=\""
    cot += time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() + 120))
    cot += "\">\n"

    cot += "<point lat=\""
    cot += str(lat)
    cot += "\" lon=\""
    cot += str(lon)
    cot += "\" hae=\""
    cot += str(feet_to_meters(alt))
    cot += "\" ce=\"9999999.0\" le=\"9999999.0\"/>\n"
    cot += "<detail>\n"
    cot += "<uid Droid=\"COT-Flight-"
    cot += str(icao)
    cot += "\"/>\n"
    cot += "<contact callsign=\""
    cot += str(callsign).strip()
    cot += "\"/>\n"
    cot += "<remarks>icao24: "
    cot += str(icao)
    cot += ", squawk: "
    cot += str(squawk)
    
    # Add country remarks if available
    if country:
        cot += " (" + country + ")"
    
    cot += "</remarks>\n"
    cot += "<track course=\""
    cot += str(round(heading))
    cot += "\" speed=\"228\"/>\n"
    cot += "</detail>\n"

    cot += "</event>\n"
    return cot

def print_aircraft(aircraft):
    if not aircraft:
        return

    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console

    print("ICAO       Callsign   Squawk     Lat        Lon        Alt")
    print("------------------------------------------------------------")

    for a in aircraft:
        icao = a.get("hex", "")
        callsign = a.get("flight", "")
        squawk = a.get("squawk", "")
        lat = a.get("lat", 0.0)
        lon = a.get("lon", 0.0)
        alt = a.get("alt_baro", 0.0)
        print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format(icao, callsign, squawk, lat, lon, alt))

def main(previous_aircraft):
    while True:
        aircraft_data = get_aircraft_data()

        # Compare the current and previous aircraft data
        new_aircraft = [a for a in aircraft_data if a not in previous_aircraft]
        removed_aircraft = [a for a in previous_aircraft if a not in aircraft_data]

        # Print updated aircraft data
        print_aircraft(aircraft_data)

        # Send CoT message over UDP for new aircraft
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        for a in new_aircraft:
            icao = a.get("hex", "")
            callsign = a.get("flight", "")
            squawk = a.get("squawk", "")
            lat = a.get("lat", 0.0)
            lon = a.get("lon", 0.0)
            alt = a.get("alt_baro", 0.0)
            heading = a.get("nav_heading", 0.0)
            if lat != 0.0 and lon != 0.0:
                cot_message = generate_cot_message(icao, callsign, squawk, lat, lon, alt, heading)
                sock.sendto(cot_message.encode(), (UDP_IP, UDP_PORT))

        # Remove the removed aircraft from previous data
        previous_aircraft = [a for a in previous_aircraft if a not in removed_aircraft]

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    previous_aircraft = []
    main(previous_aircraft)
