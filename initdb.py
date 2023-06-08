import sqlite3

# Connect to the database or create it if it doesn't exist
conn = sqlite3.connect('orders.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the "orders" table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        date TEXT,
        sum REAL,
        is_payed INTEGER,
        wallet TEXT,
        user_id TEXT
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
