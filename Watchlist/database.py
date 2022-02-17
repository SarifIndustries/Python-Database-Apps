#===============================#
# Database module for watchlist #
#===============================#

import sqlite3
import datetime

connection = sqlite3.connect("watchlist-data.db")

# Queries
CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY,
    title TEXT,
    release_timestamp REAL
);"""

CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
)
"""

CREATE_WATCHLIST_TABLE = """CREATE TABLE IF NOT EXISTS watchlist (
    user_username TEXT,
    movies_id INTEGER,
    FOREIGN KEY(user_username) REFERENCES user(username),
    FOREIGN KEY(movies_id) REFERENCES movies(id)
);"""

CREATE_RELEASE_DATE_INDEX = \
"CREATE INDEX IF NOT EXISTS idx_movie_release ON movies(release_timestamp)"

INSERT_MOVIE = "INSERT INTO movies (title, release_timestamp) VALUES (?, ?);"

INSERT_USER = "INSERT INTO users (username) VALUES (?);"

SELECT_ALL_MOVIES = "SELECT * FROM movies;"

SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;"

SELECT_WATCHED_MOVIES = """
SELECT movies.*
FROM watchlist
JOIN movies
ON movies.id = watchlist.movies_id
WHERE user_username = ?;
"""

SEARCH_MOVIES = "SELECT * FROM movies WHERE title LIKE ?;"

INSERT_MOVIE_WATCHED = "INSERT INTO watchlist (user_username, movies_id) VALUES (?, ?);"

DELETE_MOVIE = "DELETE FROM movies WHERE title = ?;"

# SET_MOVIE_WATCHED = "UPDATE watchlist SET watched = 1 WHERE title = ?;"

def create_tables():
    with connection:
        connection.execute(CREATE_MOVIES_TABLE)
        connection.execute(CREATE_USERS_TABLE)
        connection.execute(CREATE_WATCHLIST_TABLE)
        connection.execute(CREATE_RELEASE_DATE_INDEX)

def add_movie(title, release_timestamp):
    with connection:
        connection.execute(INSERT_MOVIE, (title, release_timestamp))

def add_user(username):
    with connection:
        connection.execute(INSERT_USER, (username,))

def get_movies(upcoming=False):
    cursor = connection.cursor()
    if upcoming:
        today = datetime.datetime.today().timestamp()
        cursor.execute(SELECT_UPCOMING_MOVIES, (today,))
    else:
        cursor.execute(SELECT_ALL_MOVIES)
    return cursor.fetchall()

def watch_movie(username, movie_id):
    with connection:
        connection.execute(INSERT_MOVIE_WATCHED, (username, movie_id))

def get_watched_movies(username):
    cursor = connection.cursor()
    cursor.execute(SELECT_WATCHED_MOVIES, (username,))
    return cursor.fetchall()

def search_movies(search_text):
    cursor = connection.cursor()
    cursor.execute(SEARCH_MOVIES, ("%" + search_text + "%",))
    return cursor.fetchall()
