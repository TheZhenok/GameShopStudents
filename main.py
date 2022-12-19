from flask import Flask, jsonify, request

from repository import Connection

app = Flask(__name__)

conn = Connection()

@app.route("/api/v1/main", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        return jsonify({
            "name": name,
            "lastname": lastname
        })
    return jsonify({
        "message": "Hello World!"
    })

@app.route("/api/v1/users", methods=['GET'])
def users_list():
    users = conn.users_list()
    return jsonify(users)

@app.route("/api/v1/users/save", methods=['POST'])
def user_save():
    user = request.get_json()
    print(user)
    return jsonify({
        "message": "ok"
    })

if __name__ == '__main__':
    app.run(
        host='localhost',
        port=8000,
        debug=True
    )
