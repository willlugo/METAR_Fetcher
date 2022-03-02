from argparse import MetavarTypeHelpFormatter
import requests
from datetime import datetime, timezone
from time import sleep, perf_counter

# Own Functions
import weather_requests as wreq
import weather_print as wprt
from datform import datform

# Allows the screen to be cleared
import os
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

# Key values
API_KEY = ""
BASE_URL = "https://api.checkwx.com/"
INTERVAL = 5 # Number of minutes before checking for a new METAR

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

sleep(60*INTERVAL)

# Looping METAR requests
# CHECKS EVERY INTERVAL FOR A NEW METAR
while True:
    t1_start = perf_counter()
    cls()
    wprt.print_information(info)
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

    t1_stop = perf_counter()
    sleep((60*INTERVAL)-(t1_stop-t1_start))