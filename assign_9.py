import requests
import json
import os


class WeatherForecast:

    def __init__(self):

        self.file = "weather.json"

        # load saved data
        if os.path.exists(self.file):

            with open(self.file, "r") as f:
                self.data = json.load(f)

        else:
            self.data = {}

    # save new value
    def __setitem__(self, date, weather):

        self.data[date] = weather

        with open(self.file, "w") as f:
            json.dump(self.data, f)

    # get value
    def __getitem__(self, date):

        return self.data.get(date, "No data")

    # to loop through dates
    def __iter__(self):

        for date in self.data:
            yield date

    # to loop through items
    def items(self):

        for date, weather in self.data.items():
            yield (date, weather)



weather_forecast = WeatherForecast()


# get date
date = input("Enter date (YYYY-MM-DD): ")


# check saved data
if weather_forecast[date] == "No data":

    # API request
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude=52.23&longitude=21.01"
        f"&daily=precipitation_sum"
        f"&timezone=auto" )


    response = requests.get(url)

    data = response.json()

    rain = data["daily"]["precipitation_sum"][0]

    # save data
    weather_forecast[date] = rain

else:

    rain = weather_forecast[date]


# show result
print("\nDate:", date)
print("Rain:", rain)


# show all saved dates
print("\nSaved dates:")

for d in weather_forecast:
    print(d)


# show all saved items
print("\nSaved weather data:")

for d, r in weather_forecast.items():
    print(d, "=", r)