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

    def notify_race_laps(self, season: int, round: int, delayMs: int):
        race = self.stats.get_race(season, round)
        race_laps = self.stats.laps[race["raceId"]]
        laps = race_laps[next(iter(race_laps))]

        lap = 1
        while str(lap) in laps:
            drivers = {}
            fastest_lap_ms = 1000
            for id, drivers_laps in race_laps.items():
                lap_position = f"XX{self.stats.drivers[id]['number']}"
                lap_time = "N/A"
                if str(lap) in drivers_laps:
                    lap_position = int(drivers_laps[str(lap)]["position"])
                    lap_time = drivers_laps[str(lap)]["time"]
                    lap_time_ms = int(drivers_laps[str(lap)]["milliseconds"])
                    if fastest_lap_ms < lap_time_ms:
                        fastest_lap_ms = lap_time_ms
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
            if delayMs != -1:
                time.sleep(delayMs / 1000)
            else:
                time.sleep(fastest_lap_ms / 1000)
        self.in_use = False
        print("LAPS DONE")

    def notify_standings_per_race(self, season: int, delayMs: int, drivers: bool):
        races = []
        for id, race in self.stats.races.items():
            if int(race["year"]) != season:
                continue
            races.append((int(race["round"]), id))
        races = sorted(races, key=lambda x: x[0])

        for round, id in races:
            race = self.stats.races[id]
            standings = None
            if drivers:
                standings = self.stats.get_d_championship_race_results(season, round)
            else:
                standings = self.stats.get_c_championship_race_results(season, round)
            self.send_webhook({
                "round": round,
                "race": race["name"],
                "standings": standings
            })
            time.sleep(delayMs / 1000)
        self.in_use = False
        print("DRIVERS STANDINGS DONE")


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

    def add_race_webhook(self, callback_url: str, season: int, round: int, delayMs: int):
        self._clients.append(Client(callback_url))

        thread = threading.Thread(target=self._clients[-1].notify_race_laps, args=(season, round, delayMs,))
        thread.start()

    def add_drivers_standings_webhook(self, callback_url: str, season: int, delayMs: int):
        self._clients.append(Client(callback_url))

        thread = threading.Thread(target=self._clients[-1].notify_standings_per_race, args=(season, delayMs, True,))
        thread.start()

    def add_constructors_standings_webhook(self, callback_url: str, season: int, delayMs: int):
        self._clients.append(Client(callback_url))

        thread = threading.Thread(target=self._clients[-1].notify_standings_per_race, args=(season, delayMs, False,))
        thread.start()
