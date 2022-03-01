from argparse import MetavarTypeHelpFormatter
import requests
import sys
import json

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

stations = load_stations(SAVED_STATIONS)
if len(stations) > 0:
    print("Saved Stations:\nICAO  :  Station Name")
    for key, value in stations.items():
        print(key, " : ", value)
    ICAO = input("\nInput ICAO: ").upper()
else:
    ICAO = input("Input ICAO: ").upper()

hdr = {"X-API-Key": API_KEY}

req = requests.get(f"https://api.checkwx.com/station/{ICAO}", headers=hdr)
try:
    req.raise_for_status()
    resp = req.json()
    city = resp["data"][0]["city"]
    country = resp["data"][0]["country"]["name"]
    name = resp["data"][0]["name"]
    elevation = resp["data"][0]["elevation"]["feet"]
    coordinates = resp["data"][0]["geometry"]["coordinates"]

    print(f"\nInformation for ICAO: {ICAO}")
    print(f"Aerodrome name: {name}")
    print(f"Aerodrome location: {city}, {country}")
    print(f"Longitude = {coordinates[0]} , Latitude = {coordinates[1]}")
    print(f"Aerodrome elevation: {elevation} feet")

    stations[ICAO] = name
    save_stations(SAVED_STATIONS, stations)

except requests.exceptions.HTTPError as e:
    print(e)

req = requests.get(f"https://api.checkwx.com/metar/{ICAO}/decoded", headers=hdr)
try:
    req.raise_for_status()
    response = req.json()
    
    if len(response["data"]) != 1:
        print("\nNo METAR data found\n")
        x = input("Press Enter to exit: ")
        quit()
    metar = response["data"][0]
    
    print(f"\nCurrent weather at {name}:")

    observed = metar["observed"]
    print(f"    Observed: {observed}")

    if "wind" in metar:
        print(f"    Wind:")
        wind = metar["wind"]
        if "degrees" in wind:
            direc = str(wind["degrees"]).zfill(3)
            print(f"        Direction: {direc:3} degrees")
        else:
            print("        No wind direction found")
        if "speed_kts" in wind:
            speed = wind["speed_kts"]
            print(f"        Speed:     {speed:3} kts")
        else:
            print("        No wind speed information found")
        if "gust_kts" in wind:
            gust = wind["gust_kts"]
            print(f"        Gusting:   {gust} kts")
        else:
            print("        No wind gust information found")
    else:
        print("    No wind information found")
    
    if "visibility" in metar:
        vis = metar["visibility"]
        if "meters" in vis:
            vism = vis["meters"]
            print(f"    Visibility: {vism} meters")
    else:
        print("    Visibility information not found")
    
    if "conditions" in metar:
        conditions = metar["conditions"]
        print("    Conditions:")
        for i in conditions:
            if "prefix" in i:
                prefix = i["prefix"]
            else:
                prefix = ""
            if "code" in i:
                code = i["code"]
            else:
                code = ""
            if "text" in i:
                text = i["text"]
            else:
                text = ""
            print(f"        {prefix:>3}{code:<4}, {text}")
    else:
        print("    No conditions information found")
    
    if "clouds" in metar:
        print("    Clouds:")
        clouds = metar["clouds"]
        for i in clouds:
            if "feet" in i:
                feet = i["feet"]
                if "code" in i:
                    code = i["code"]
                else:
                    code = ""
                if "text" in i:
                    text = i["text"]
                else:
                    text = ""
                print(f"        {feet:5} ft, {code:5}, {text}")
            else:
                if "code" in i:
                    code = i["code"]
                    if "text" in i:
                        text = i["text"]
                    else:
                        text = ""
                else:
                    code = ""
                print(f"        {code:5}, {text}")
    else:
        print("    No cloud information found")

    if "barometer" in metar:
        bar = metar["barometer"]
        if "hpa" in bar:
            bar_hpa = bar["hpa"]
            print(f"    Barometer: {bar_hpa} hpa")
    else:
        print("    Barometer reading not found")
    
    if "temperature" in metar:
        temperature = metar["temperature"]
        if "celsius" in temperature:
            temperature_c = temperature["celsius"]
            print(f"    Temperature: {temperature_c} degrees celsius")

    if "flight_category" in metar:
        flight_category = metar["flight_category"]
        print(f"    Current flight conditions: {flight_category}")
    else:
        print("    Flight condition code not found")
    
    raw_met = metar["raw_text"]
    print("\n    Raw METAR:")
    print(f"        {raw_met}")

except requests.exceptions.HTTPError as e:
    print(e)

print("\n")
x = None
while x == None:
    x = input("Press Enter to exit: ")