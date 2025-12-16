import csv
from importlib import resources as impres
from . import data  # pyright: ignore[reportAttributeAccessIssue]

#from pprint import pprint


class Statistics:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.seasons: dict[str, dict[str, str]] = self.load_csv_to_dict("seasons.csv", "year")
        self.circuits: dict[str, dict[str, str]] = self.load_csv_to_dict("circuits.csv", "circuitId")

        self.races: dict[str, dict[str, str]] = self.load_csv_to_dict("races.csv", "raceId")
        self.results: dict[str, dict[str, str]] = self.load_csv_to_dict("results.csv", "resultId")
        self.laps: dict[str, dict[str, dict[str, str]]] = self.load_csv_to_laps("lap_times.csv")

        self.drivers: dict[str, dict[str, str]] = self.load_csv_to_dict("drivers.csv", "driverId")
        self.constructors: dict[str, dict[str, str]] = self.load_csv_to_dict("constructors.csv", "constructorId")

        self.driver_standings: dict[str, dict[str, str]] = self.load_csv_to_dict("driver_standings.csv", "driverStandingsId")
        self.constructor_standings: dict[str, dict[str, str]] = self.load_csv_to_dict("constructor_standings.csv", "constructorStandingsId")


    def load_csv_to_dict(self, file_name: str, id_column: str):
        file = impres.files(data) / file_name
        with file.open("r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            return {row[id_column]: row for row in reader}

    def load_csv_to_laps(self, file_name: str):
        file = impres.files(data) / file_name
        with file.open("r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            result = {}
            for row in reader:
                if row["raceId"] not in result:
                    result[row["raceId"]] = {}
                if row["driverId"] not in result[row["raceId"]]:
                    result[row["raceId"]][row["driverId"]] = {}
                if row["lap"] not in result[row["raceId"]][row["driverId"]]:
                    result[row["raceId"]][row["driverId"]][row["lap"]] = {
                        "position": row["position"],
                        "time": row["time"],
                        "milliseconds": row["milliseconds"]
                    }
            #pprint(result["1134"])
            return result


    def get_driver_by_surname(self, surname: str) -> list[dict[str, str]]:
        result = []
        for id, driver in self.drivers.items():
            if driver["surname"] == surname:
                result.append(driver)
        return result

    def get_race(self, year: int, round: int) -> dict[str, str]:
        print(f"{year} {round}")
        for id, race in self.races.items():
            if int(race["year"]) == year and int(race["round"]) == round:
                return race
        raise ValueError("Race not found")

    def get_race_results(self, year: int, round: int):
        race_id = self.get_race(year, round)["raceId"]

        results = {}
        for id, result in self.results.items():
            if result["raceId"] != race_id:
                continue
            results[result["position"]] = {
                "driver": self.drivers[result["driverId"]]["driverRef"].title(),
                "constructor": self.constructors[result["constructorId"]]["name"],
                "grid": result["grid"]
            }
        return results

    def get_seasons(self):
        results = []
        for id, seasons in self.seasons.items():
            results.append(id)
        results.sort()
        return results

    def get_season_races(self, year: int):
        results = {}
        for id, race in self.races.items():
            if race["year"] != year:
                continue
            results[race["round"]] = {
                "name": race["name"],
                "date": race["date"]
            }
        return results


    def get_d_championship_race_results(self, season: int, round: int):
        race_id = self.get_race(season, round)["raceId"]

        results = {}
        for id, d_standing in self.driver_standings.items():
            if d_standing["raceId"] != race_id:
                continue
            results[d_standing["position"]] = {
                "points": d_standing["points"],
                "driver": self.drivers[d_standing["driverId"]]["driverRef"].title(),
                "wins": d_standing["wins"]
            }
        return results

    def get_c_championship_race_results(self, season: int, round: int):
        race_id = self.get_race(season, round)["raceId"]

        results = {}
        for id, c_standing in self.constructor_standings.items():
            if c_standing["raceId"] != race_id:
                continue
            results[c_standing["position"]] = {
                "points": c_standing["points"],
                "driver": self.constructors[c_standing["constructorId"]]["name"],
                "wins": c_standing["wins"]
            }
        return results
