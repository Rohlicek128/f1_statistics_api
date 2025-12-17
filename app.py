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
@app.route('/api/v1/stats/drivers/<string:surname>', methods=['GET'])
def stats_driver(surname):
    return json.dumps(stats.get_driver_by_surname(surname))


# Seasons
@app.route('/api/v1/stats/seasons', methods=['GET'])
def stats_seasons():
    return json.dumps(stats.get_seasons())

@app.route('/api/v1/stats/seasons/<int:season>/races', methods=['GET'])
def stats_seasons_races(season):
    return json.dumps(stats.get_season_races(int(season)))

@app.route('/api/v1/stats/seasons/<int:season>/races/<int:round>/results', methods=['GET'])
def stats_seasons_race_results(season, round):
    return json.dumps(stats.get_race_results(int(season), int(round)))

#Championships
@app.route('/api/v1/stats/seasons/<int:season>/championships/drivers', methods=['GET'])
def stats_seasons_d_championship(season):
    round = request.args.get("round", type=int)
    try:
        if round is None:
            round = sorted(map(lambda x : int(x), list(stats.get_season_races(season).keys())))[-1]

        return json.dumps(stats.get_d_championship_race_results(int(season), int(round)))
    except:
        abort(400)

@app.route('/api/v1/stats/seasons/<int:season>/championships/constructors', methods=['GET'])
def stats_seasons_c_championship(season):
    round = request.args.get("round", type=int)
    try:
        if round is None:
            round = sorted(map(lambda x : int(x), list(stats.get_season_races(season).keys())))[-1]

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
    app.run(host="127.0.0.1", port=8088, debug=False)
