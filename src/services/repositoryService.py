import sqlite3
import os

def initCursor():
    conn = sqlite3.connect(os.path.abspath("../../orders.db"))
    return conn.cursor()