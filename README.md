# METAR_Fetcher
Simple project to use the checkWX API in order to fetch airfield information and current weather information for any aerodrome with an ICAO code.

Own API key needed

Steps:
Insert own API key into the program.
Ensure all internal modules are in the same directory as the program.
Use pip to install all required external modules.
Open command prompt to directory containing modules and program.
Use pyinstaller to convert the program to an executable using the following syntax:
    pyinstaller --onefile program_name.py
Exexutable file will be in a new dist directory

currently three modules:
    datform.py
    weather_print.py
    weather_requests.py

three programs:
    any_metar_sterile.py
    any_metar_options_sterile.py
    updating_METAR_sterile.py