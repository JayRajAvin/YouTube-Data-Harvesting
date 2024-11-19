import sqlite3
import pandas as pd


def drop_tables():
    conn = sqlite3.connect('youtube_data.db')
    cursor = conn.cursor()

    # Drop the tables if they exist
    cursor.execute('DROP TABLE IF EXISTS channels;')
    cursor.execute('DROP TABLE IF EXISTS videos;')
    cursor.execute('DROP TABLE IF EXISTS comments;')

    conn.commit()
    conn.close()

# Call the function to drop the tables
drop_tables()