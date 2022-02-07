#=================================#
# Database module for progjournal #
#=================================#

import sqlite3


# Connect or create new database file
connection = sqlite3.connect("journal.db")

# Optional: create rows similar to dictionaires.
# Otherwise cursor elements are tuples.
connection.row_factory = sqlite3.Row


def create_table_if_not_exists():
	query = "CREATE TABLE IF NOT EXISTS entries (date_stamp TEXT, content TEXT);"
	connection.execute(query)
	connection.commit() # Commit whole transaction
	# Alternative construct:
	# with connection:
	#	connection.execute(<...>)


# Allows SQL Injection
def storage_add_insecure(date: str, content: str):
	query = f"INSERT INTO entries (date_stamp, content) VALUES ('{date}', '{content}');"
	connection.execute(query)
	connection.commit()

# Prevents SQL Injection
def storage_add(date: str, content: str):
	query = "INSERT INTO entries (date_stamp, content) VALUES (?, ?);"
	params_cortage = (date, content)
	connection.execute(query, params_cortage)
	connection.commit()

def storage_get():
	query = "SELECT date_stamp, content FROM entries"
	cursor = connection.execute(query)
	return cursor # Iterable. Or: cursor.fetchall() // .fetchone()
