from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
_ = CORS(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000, debug=False)
