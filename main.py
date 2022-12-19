from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify("bingo")

if __name__ == '__main__':
    app.run(
        host='localhost',
        port=8000,
        debug=True
    )
