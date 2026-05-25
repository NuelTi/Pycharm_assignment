import os
import requests
import json
from datetime import datetime, timedelta

# ---------- SETTINGS ----------
# Warsaw, Poland coordinates
latitude = 52.2297
longitude = 21.0122

# File where results will be saved
FILE_NAME = "weather_data.json"


# ---------- LOAD SAVED DATA ---------- #
if os.path.exists(FILE_NAME):
    try:
        with open(FILE_NAME, "r") as file:
            saved_data = json.load(file)
    except:
        saved_data = {}
else:
    saved_data = {}


# ---------- GET DATE FROM USER ---------- #
date_input = input("Enter date (YYYY-mm-dd) or press ENTER for tomorrow: ")

if date_input == "":
    tomorrow = datetime.now() + timedelta(days=1)
    searched_date = tomorrow.strftime("%Y-%m-%d")
else:
    try:
        # check if date format is correct
        datetime.strptime(date_input, "%Y-%m-%d")
        searched_date = date_input
    except:
        print("Invalid date format. Check correct format")
        exit()


# ---------- CHECK SAVED DATA ----------
if searched_date in saved_data:
    print("\nData loaded from file.")

    precipitation = saved_data[searched_date]

else:
    # ---------- API REQUEST ---------- #
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&daily=precipitation_sum"
        f"&timezone=Europe%Warsaw"
        f"&start_date={searched_date}"
        f"&end_date={searched_date}"
    )

    try:
        response = requests.get(url)
        data = response.json()

        precipitation_list = data["daily"]["precipitation_sum"]

        if len(precipitation_list) > 0:
            precipitation = precipitation_list[0]
        else:
            precipitation = -1

        # save result to file
        saved_data[searched_date] = precipitation

        with open(FILE_NAME, "w") as file:
            json.dump(saved_data, file)

    except:
        print("Error while connecting to API.")
        exit()


# ---------- DISPLAY RESULT ---------- #
print("\nCity: Warsaw, Poland")
print("Date:", searched_date)

if precipitation > 0.0:
    print("It will rain.")
    print("Precipitation:", precipitation, "mm")

elif precipitation == 0.0:
    print("It will not rain.")

else:
    print("I don't know.")