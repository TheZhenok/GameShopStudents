from flask import Flask, request, abort, jsonify
from services import Connection
import json



app = Flask(__name__)
conn: Connection = Connection()
conn.create_tables()


@app.route('/game', methods=['POST','GET'])
def main():
    form = request.get_json()
    game_title = form['game']
    game_img = form['img']
    game_price = form['price']
    game_count = form['count']
    game_description = form['description']
    game_rate = form['rate']
    if game_title and game_img and game_price and game_count and game_description and game_rate:
        # adding game to database
        new_game_id = conn.adding_to_game(game_title,game_img,game_price,game_count,game_description,game_rate)
        # creating game code
        conn.adding_to_gamecode(new_game_id[0])
        # selecting generated game code
        game_code = conn.select_code_from_game(new_game_id[0])
        return jsonify ({'Adding to game database': 'success','game_title': game_title, 
        'image': game_img, 'price':game_price, 'count':game_count, 'description': game_description, 'rate': game_rate, 'game_code': game_code[0]})
    else:
        return jsonify({'An error occured': 'fill all forms'})

@app.route('/user', methods=['POST','GET'])
def user():
    form = request.get_json()
    username = form['user']
    password = form['password']
    money = form['money']
    if username and password:
        # adding new user credentials to database
        conn.add_user_to_database(username, password, money)
        return jsonify({'Adding to username database': 'success', 'username': username, 'password': password, 'money': money})
    else:
        return jsonify({'An error occured': 'fill all forms'})

@app.route('/all_registered_users', methods = ['POST', 'GET'])
def show_users():
    # showing all users in database
    show_users = conn.show_user_database()
    user = [item[0] for item in show_users]
    json_user = json.dumps(user)
    return jsonify({'All users in database': json_user})

@app.route('/show_friends', methods = ['POST', 'GET'])
def show_friends():
    form = request.get_json()
    username = form['user']
    # showing all users except entered 
    current_user_id = conn.user_return_id(username)
    select_friends = conn.select_friend_from_id(current_user_id[0])
    
    return jsonify({"All user's friends": select_friends})

@app.route('/user_login', methods=['POST','GET'])
def user_check():
    form = request.get_json()
    username = form['user']
    password = form['password']
    # checking user in database
    global check_user
    check_user = conn.username_check(username)
    check_password = conn.select_password_from_user(check_user[0])
    if check_user[0] and password == check_password[0]:
        return jsonify({'User found': 'success'})
    else:
        return jsonify({'An error occured': 'user not found'})

@app.route('/shop', methods=['POST','GET'])
def user_buy():
    form = request.get_json()
    username = form['user']
    check_user = conn.username_check(username)
    select_game = form['game']
    game_count = form['count']
    if check_user:
        game_id = conn.select_game(select_game)
        user_id = conn.user_return_id(check_user[0])
        if game_count > game_id[3]:
            return jsonify({'Info':"game count is less"})
        conn.insert_to_orders(user_id[0],game_id[0])
        check_user_money = conn.username_check_money(check_user[0])
        if check_user_money[0] < game_id[2]:
            return jsonify({"Info":"not enought money"})
        conn.buying_game(check_user[0],game_id[2], game_count)
        game_code = conn.select_code_from_game(game_id[0])
        conn.buying_game_count(select_game,game_count)
        return jsonify({"You're selected game to buy": select_game, "Game price": game_id[2], "Game code": game_code})
    return jsonify({'Info':'An error occurred!'})

if __name__ == '__main__':
    app.run(port=8080, debug=True)
