import requests

def get_information(BASE_URL,API_KEY,ICAO):
    hdr = {"X-API-Key": API_KEY}
    return requests.get(f"{BASE_URL}station/{ICAO}", headers=hdr)


def get_metar(BASE_URL,API_KEY,ICAO):
    hdr = {"X-API-Key": API_KEY}
    return requests.get(f"{BASE_URL}metar/{ICAO}/decoded", headers=hdr)