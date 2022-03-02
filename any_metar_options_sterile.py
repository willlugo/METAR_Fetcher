from argparse import MetavarTypeHelpFormatter
import requests
import sys
import json

# Own Functions
import weather_requests as wreq
import weather_print as wprt
from datform import datform

API_KEY = ""
BASE_URL = "https://api.checkwx.com/"

SAVED_STATIONS = "station_history.json"
def save_stations(filepath, stations):
    with open(filepath, "w") as f:
        json.dump(stations, f)

def load_stations(filepath):
    try:
        with open(filepath, "r") as f:
            stations = json.load(f)
            return stations
    except:
        return {}

# LOAD SAVED STATIONS FROM JSON FILE AND PRINT TO CONSOLE IF THEY EXIST
stations = load_stations(SAVED_STATIONS)
if len(stations) > 0:
    print("Saved Stations:\nICAO  :  Station Name")
    for key, value in stations.items():
        print(key, " : ", value)
    print()

# GET AERODROME IDENTIFIER FROM USER
ICAO = input("Input ICAO: ").upper()

# GET AIRFIELD INFORMATION AND PRINT TO CONSOLE
inf_req = wreq.get_information(BASE_URL,API_KEY,ICAO)
try:
    inf_req.raise_for_status()
    info = inf_req.json()
    wprt.print_information(info)
    stations[ICAO] = name
    save_stations(SAVED_STATIONS, stations)
except requests.exceptions.HTTPError as e:
    print(e)

# GET METAR AND PRINT TO CONSOLE 
met_req = wreq.get_metar(BASE_URL,API_KEY,ICAO)
try:
    met_req.raise_for_status()
    met_response = met_req.json()
    if len(met_response["data"]) == 1:
        metar = met_response["data"][0]
        wprt.print_metar(metar)
    else:
        dtnow = datform()
        print(f"\nNo METAR data found: {dtnow}\n")
except requests.exceptions.HTTPError as e:
    print(e)

print("\n")
x = None
while x == None:
    x = input("Press Enter to exit: ")