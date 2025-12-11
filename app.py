from flask import Flask, request, abort
from flask_cors import CORS

from f1stats import Statistics, WebhooksManager
import json
#from pprint import pprint

app = Flask(__name__)
_ = CORS(app)

stats = Statistics()
webhookManager = WebhooksManager()


@app.route('/', methods=['GET'])
def index():
    return "nope"


@app.route('/api/v1/stats/drivers', methods=['GET'])
def stats_driver():
    data = request.get_json()
    if "surname" not in data:
        abort(400)
    return json.dumps(stats.get_driver_by_surname(data["surname"]))

@app.route('/api/v1/stats/seasons/races/results', methods=['GET'])
def stats_race_results():
    data = request.get_json()
    return json.dumps(stats.get_race_results(int(data["season"]), int(data["round"])))


# Webhook
@app.route('/api/v1/stats/seasons/races/active/hook', methods=['GET'])
def stats_race_results_wh():
    data = request.get_json()
    if "callbackUrl" not in data:
        abort(400)
    webhookManager.add_client(data["callbackUrl"])
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/dev/hooks', methods=['POST'])
def dev_hooks():
    data = request.get_json()
    print(data)
    return "Accepted"


if __name__ == "__main__":
    #pprint(stats.get_driver_by_surname("Piastri"))
    #pprint(stats.get_race(1980, 10))
    #pprint(stats.get_race_results(1980, 10))
    app.run(host="172.20.10.7", port=8088, debug=False)
