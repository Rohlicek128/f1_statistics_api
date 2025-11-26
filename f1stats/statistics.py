import csv
from importlib import resources as impres
from . import data  # pyright: ignore[reportAttributeAccessIssue]


class Statistics:
    def __init__(self) -> None:
        self.seasons: dict[str, dict[str, str]] = self.load_csv_to_dict("seasons.csv", "year")
        self.circuits: dict[str, dict[str, str]] = self.load_csv_to_dict("circuits.csv", "circuitId")
        self.races: dict[str, dict[str, str]] = self.load_csv_to_dict("races.csv", "raceId")
        self.results: dict[str, dict[str, str]] = self.load_csv_to_dict("results.csv", "resultId")
        self.drivers: dict[str, dict[str, str]] = self.load_csv_to_dict("drivers.csv", "driverId")


    def load_csv_to_dict(self, file_name: str, id_column: str):
        file = impres.files(data) / file_name
        with file.open("r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            return {row[id_column]: row for row in reader}


    def get_driver_by_surname(self, surname: str):
        result = []
        for id, driver in self.drivers.items():
            if driver["surname"] == surname:
                result.append(driver)
        return result

    def get_race(self, year: int, round: int):
        for id, race in self.races.items():
            if int(race["year"]) == year and int(race["round"]) == round:
                return race
        raise ValueError("Race not found")

    def get_race_results(self, year: int, round: int):
        race_id = self.get_race(year, round)["raceId"]

        results = []
        for id, result in self.results.items():
            if result["raceId"] != race_id:
                continue
            results.append((result["position"], self.drivers[result["driverId"]]["surname"]))

        return results
