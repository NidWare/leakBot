import sqlite3
import datetime
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(current_dir, '..', '..')

# Construct the path to the SQLite database file
db_path = os.path.join(root_dir, 'orders.db')


def delete_old_records():
    # establish a connection to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # define the time interval for deletion (last hour from the current time)
    current_time = datetime.datetime.now()
    one_hour_ago = current_time - datetime.timedelta(hours=1)
    one_hour_ago_str = one_hour_ago.strftime('%Y-%m-%d %H:%M:%S')

    # delete records from the database where the date is earlier than the specified interval
    cursor.execute("DELETE FROM orders WHERE date < ?", (one_hour_ago_str,))
    conn.commit()

    # close the database connection
    cursor.close()
    conn.close()


delete_old_records()