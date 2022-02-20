# Add comment

import os
import psycopg2
import dotenv

dotenv.load_dotenv()

PALISADE_URL = os.environ["PALISADE_URL"]

QUERY = "SELECT * FROM heroes;"

connection = psycopg2.connect(PALISADE_URL)

cursor = connection.cursor()

cursor.execute(QUERY)

row = cursor.fetchone()

print(row)
