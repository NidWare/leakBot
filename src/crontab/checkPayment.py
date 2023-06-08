import sqlite3
import datetime
import os
import sys

# Get the absolute path of the directory where checkPayment.py is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the services directory
services_dir = os.path.join(current_dir, '..', 'services')

# Add the services directory to sys.path
sys.path.append(os.path.join(current_dir, '..', 'services'))

# Import the tronService module
import tronService

root_dir = os.path.join(services_dir, '..', '..')

# Construct the path to the SQLite database file
db_path = os.path.join(root_dir, 'orders.db')


# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT * FROM orders WHERE is_payed = 0 LIMIT 30")

for order in cursor.fetchall():
    timestamp = order[1]

    print("Start checking transaction with params: {}, {}, {}".format(str(order[4]), str(order[2]), str(timestamp)))
    if tronService.check_incoming_transactions(order[4], order[2], timestamp):
        cursor.execute("UPDATE orders SET is_payed = 1 WHERE id = '{}'".format(order[0]))
        conn.commit()
