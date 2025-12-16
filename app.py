from flask import Flask, request, abort
from flask_cors import CORS

from f1stats import Statistics, WebhooksManager
import json
from pprint import pprint


app = Flask(__name__)
_ = CORS(app)

stats = Statistics()
webhookManager = WebhooksManager()


@app.route('/', methods=['GET'])
def index():
    return "coconut.jpg"


# Drivers
@app.route('/api/v1/stats/drivers', methods=['GET'])
def stats_driver():
    data = request.get_json()
    if "surname" not in data:
        abort(400)
    return json.dumps(stats.get_driver_by_surname(data["surname"]))


# Seasons
@app.route('/api/v1/stats/seasons', methods=['GET'])
def stats_seasons():
    return json.dumps(stats.get_seasons())

@app.route('/api/v1/stats/seasons/races', methods=['GET'])
def stats_seasons_races():
    data = request.get_json()
    if "season" not in data:
        abort(400)
    return json.dumps(stats.get_season_races(data["season"]))

@app.route('/api/v1/stats/seasons/races/results', methods=['GET'])
def stats_seasons_race_results():
    data = request.get_json()
    if "season" not in data or "round" not in data:
        abort(400)
    return json.dumps(stats.get_race_results(int(data["season"]), int(data["round"])))

#Championships
@app.route('/api/v1/stats/seasons/championships/drivers', methods=['GET'])
def stats_seasons_d_championship():
    data = request.get_json()
    season = None
    round = None
    try:
        if "season" not in data:
            abort(400)
        else:
            season = data["season"]

        if "round" not in data:
            round = sorted(map(lambda x : int(x), list(stats.get_season_races(season).keys())))[-1]
        else:
            round = data["round"]
        return json.dumps(stats.get_d_championship_race_results(int(season), int(round)))
    except:
        abort(400)

@app.route('/api/v1/stats/seasons/championships/constructors', methods=['GET'])
def stats_seasons_c_championship():
    data = request.get_json()
    season = None
    round = None
    try:
        if "season" not in data:
            abort(400)
        else:
            season = data["season"]

        if "round" not in data:
            round = sorted(map(lambda x : int(x), list(stats.get_season_races(season).keys())))[-1]
        else:
            round = data["round"]
        return json.dumps(stats.get_c_championship_race_results(int(season), int(round)))
    except:
        abort(400)


# Webhooks
@app.route('/api/v1/stats/seasons/races/active/hook', methods=['POST'])
def stats_race_results_wh():
    data = request.get_json()
    if "callbackUrl" not in data or "season" not in data or "round" not in data:
        abort(400)
    webhookManager.add_client(data["callbackUrl"], season=int(data["season"]), round=int(data["round"]))
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/dev/hooks', methods=['POST'])
def dev_hooks():
    data = request.get_json()
    pprint(data)
    return "Accepted"


if __name__ == "__main__":
    #pprint(stats.get_driver_by_surname("Piastri"))
    #pprint(stats.get_race(1980, 10))
    #pprint(stats.get_race_results(1980, 10))
    app.run(host="127.0.0.1", port=8088, debug=False)
