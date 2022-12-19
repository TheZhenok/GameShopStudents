CREATE DATABASE IF NOT EXISTS gameshop;

CREATE TABLE IF NOT EXISTS games(
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    img TEXT,
    price INTEGER NOT NULL DEFAULT 0,
    count INTEGER,
    descr TEXT,
    rate INTEGER
);

CREATE TABLE IF NOT EXISTS gamecodes(
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    code TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    email VARCHAR(100),
    pass VARCHAR(50),
    wallet INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS userfriends(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    friend_id INTEGER REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS orders(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    game_id INTEGER REFERENCES games(id),
    price INTEGER,
    count INTEGER,
    date_buying TIMESTAMP DEFAULT(CURRENT_TIMESTAMP)
);

CREATE TABLE IF NOT EXISTS transactions(
    id SERIAL PRIMARY KEY,
    descr TEXT,
    user_id INTEGER REFERENCES users(id),
    date_exec TIMESTAMP DEFAULT(CURRENT_TIMESTAMP)
);





