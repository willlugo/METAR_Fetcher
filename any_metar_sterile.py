from argparse import MetavarTypeHelpFormatter
import requests
from datetime import datetime, timezone
from time import sleep, perf_counter

# Own Functions
import weather_requests as wreq
import weather_print as wprt
from datform import datform

# Key values
API_KEY = ""
BASE_URL = "https://api.checkwx.com/"

# Get aerodrome identifier from user
ICAO = input("Input ICAO: ").upper()

# GET AIRFIELD INFORMATION AND PRINT TO CONSOLE
inf_req = wreq.get_information(BASE_URL,API_KEY,ICAO)
try:
    inf_req.raise_for_status()
    info = inf_req.json()
    wprt.print_information(info)
except requests.exceptions.HTTPError as e:
    print(e)

# First METAR request
# PRINT METAR TO CONSOLE
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