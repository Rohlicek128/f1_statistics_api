from flask import Flask, request, render_template
from flask_cors import CORS

from f1stats import Statistics
import json
#from pprint import pprint

app = Flask(__name__)
_ = CORS(app)

stats = Statistics()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/api/v1/stats/drivers', methods=['GET'])
def stats_driver():
    data = request.get_json()
    return json.dumps(stats.get_driver_by_surname(data["surname"]))

@app.route('/api/v1/stats/races/results', methods=['GET'])
def stats_race_results():
    data = request.get_json()
    return json.dumps(stats.get_race_results(int(data["year"]), int(data["round"])))


if __name__ == "__main__":
    #pprint(stats.get_driver_by_surname("Piastri"))
    #pprint(stats.get_race(1980, 10))
    #pprint(stats.get_race_results(1980, 10))
    app.run(host="127.0.0.1", port=3000, debug=False)
