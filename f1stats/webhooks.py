import requests
import time
import threading
#from pprint import pprint

from .statistics import Statistics

class Client:
    def __init__(self, callback_url: str):
        self.callback_url: str = callback_url
        self.in_use: bool = True
        self.stats = Statistics()

    def notify_race_laps(self, season: int, round: int):
        race = self.stats.get_race(season, round)
        race_laps = self.stats.laps[race["raceId"]]
        laps = race_laps[next(iter(race_laps))]

        lap = 1
        while str(lap) in laps:
            drivers = {}
            for id, drivers_laps in race_laps.items():
                lap_position = "XX"
                lap_time = "N/A"
                if str(lap) in drivers_laps:
                    lap_position = int(drivers_laps[str(lap)]["position"])
                    lap_time = drivers_laps[str(lap)]["time"]
                drivers["{:02}".format(lap_position)] = {
                    "driver": self.stats.drivers[id]["driverRef"].title(),
                    "time": lap_time
                }

            self.send_webhook({
                "race": race["name"],
                "lap": lap,
                "drivers": drivers
            })
            lap += 1
            time.sleep(1)
        self.in_use = False
        print("LAPS DONE")


    def send_webhook(self, json):
        try:
            return requests.post(
                self.callback_url,
                headers={"Content-Type": "application/json"},
                json=json,
                timeout=10
            )
        except requests.exceptions.Timeout as err:
            print(err)
            return err

class WebhooksManager:
    def __init__(self):
        self._clients: list[Client] = []

    def add_client(self, callback_url: str, **kvargs):
        self._clients.append(Client(callback_url))

        thread = threading.Thread(target=self._clients[-1].notify_race_laps, args=(kvargs["season"], kvargs["round"],))
        thread.start()
