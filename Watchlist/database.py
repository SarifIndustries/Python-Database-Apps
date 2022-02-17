#===============================#
# Database module for watchlist #
#===============================#

import sqlite3
import datetime

connection = sqlite3.connect("watchlist-data.db")

# Queries
CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
	title TEXT,
	release_timestamp REAL
);"""

CREATE_WATCHLIST_TABLE = """CREATE TABLE IF NOT EXISTS watchlist (
	watcher_name TEXT,
	title TEXT
);"""

INSERT_MOVIE = "INSERT INTO movies (title, release_timestamp) VALUES (?, ?);"

SELECT_ALL_MOVIES = "SELECT * FROM movies;"

SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;"

SELECT_WATCHED_MOVIES = "SELECT * FROM watchlist WHERE watcher_name = ?;"

INSERT_MOVIE_WATCHED = "INSERT INTO watchlist (watcher_name, title) VALUES (?, ?);"

DELETE_MOVIE = "DELETE FROM movies WHERE title = ?;"

# SET_MOVIE_WATCHED = "UPDATE watchlist SET watched = 1 WHERE title = ?;"

def create_tables():
	with connection:
		connection.execute(CREATE_MOVIES_TABLE)
		connection.execute(CREATE_WATCHLIST_TABLE)

def add_movie(title, release_timestamp):
	with connection:
		connection.execute(INSERT_MOVIE, (title, release_timestamp))

def get_movies(upcoming=False):
	cursor = connection.cursor()
	if upcoming:
		today = datetime.datetime.today().timestamp()
		cursor.execute(SELECT_UPCOMING_MOVIES, (today,))
	else:
		cursor.execute(SELECT_ALL_MOVIES)
	return cursor.fetchall()

def watch_movie(username, title):
	with connection:
		connection.execute(DELETE_MOVIE, (title,))
		connection.execute(INSERT_MOVIE_WATCHED, (username, title))

def get_watched_movies(username):
	cursor = connection.cursor()
	cursor.execute(SELECT_WATCHED_MOVIES, (username,))
	return cursor.fetchall()
