# Zinchenko Bogdan | 19.12.2022 19:09
# siuuu

from flask import (
    Flask,
    request,
    jsonify,
)


app = Flask(__name__)

@app.route('/api/v1/main', methods=['POST', 'GET'])
def main_route():
    if request.method == 'POST':
        data: dict[str: Any] = request.get_json()
        var_one = data.get('name')
        var_two = data.get('lastname')
        return jsonify({
            'var1' : var_one,
            'var2' : var_two,
        })
    return  jsonify({'hi' : 'world'})

if __name__ == '__main__':
    app.run(debug=True, port=5050)