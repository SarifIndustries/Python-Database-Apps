# ================================#
#  Database module for watchlist  #
# ================================#

import os
import psycopg2
import dotenv
import datetime


CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
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
    FOREIGN KEY(user_username) REFERENCES users(username),
    FOREIGN KEY(movies_id) REFERENCES movies(id)
);"""

CREATE_RELEASE_DATE_INDEX = \
    "CREATE INDEX IF NOT EXISTS idx_movie_release ON movies(release_timestamp)"

INSERT_MOVIE = "INSERT INTO movies (title, release_timestamp) VALUES (%s, %s);"

INSERT_USER = "INSERT INTO users (username) VALUES (%s);"

SELECT_ALL_MOVIES = "SELECT * FROM movies;"

SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > %s;"

SELECT_WATCHED_MOVIES = """
SELECT movies.*
FROM watchlist
JOIN movies
ON movies.id = watchlist.movies_id
WHERE user_username = %s;
"""

SEARCH_MOVIES = "SELECT * FROM movies WHERE title LIKE %s;"

INSERT_MOVIE_WATCHED = "INSERT INTO watchlist (user_username, movies_id) VALUES (%s, %s);"

DELETE_MOVIE = "DELETE FROM movies WHERE title = %s;"


global connection


def establish_connection():
    global connection
    dotenv.load_dotenv()
    url = os.environ["PALISADE_URL"]
    connection = psycopg2.connect(url)


def close_connection():
    connection.close()


def create_tables():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_MOVIES_TABLE)
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(CREATE_WATCHLIST_TABLE)
            cursor.execute(CREATE_RELEASE_DATE_INDEX)


def add_movie(title, release_timestamp):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MOVIE, (title, release_timestamp))


def add_user(username):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER, (username,))


def get_movies(upcoming=False):
    with connection:
        with connection.cursor() as cursor:
            if upcoming:
                today = datetime.datetime.today().timestamp()
                cursor.execute(SELECT_UPCOMING_MOVIES, (today,))
            else:
                cursor.execute(SELECT_ALL_MOVIES)
            return cursor.fetchall()


def watch_movie(username, movie_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MOVIE_WATCHED, (username, movie_id))


def get_watched_movies(username):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_WATCHED_MOVIES, (username,))
            return cursor.fetchall()


def search_movies(search_text):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SEARCH_MOVIES, ("%" + search_text + "%",))
            return cursor.fetchall()
