import sqlite3
import pandas as pd
import streamlit as st

DATABASE_NAME = 'youtube_data.db'

def create_tables():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS channels (
            channel_id TEXT PRIMARY KEY,
            name TEXT,
            channel_desc TEXT,
            subscriber_count INTEGER,
            video_count INTEGER,
            view_count INTEGER,
            playlist_id TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            video_id TEXT PRIMARY KEY,
            channel_id TEXT,
            video_name TEXT,
            video_desc TEXT,
            published_at DATETIME,
            views INTEGER,
            likes INTEGER,
            comments INTEGER,
            duration INTEGER,
            thumbnail TEXT,
            caption TEXT,
            FOREIGN KEY (channel_id) REFERENCES channels(channel_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            comment_id TEXT PRIMARY KEY,
            video_id TEXT,
            comment_text TEXT,
            author TEXT,
            comment_published_date DATETIME,
            FOREIGN KEY (video_id) REFERENCES videos(video_id)
        )
    ''')
    conn.commit()
    conn.close()

def save_data_to_database(channel_data, video_data, comment_data):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    try:
        # Check for duplicate channel
        cursor.execute("SELECT channel_id FROM channels WHERE channel_id = ?", (channel_data["channel_id"],))
        if cursor.fetchone():
            return {"duplicate_channel": channel_data["channel_id"]}  # Return duplicate channel ID        
        
        # Save channel data
        cursor.execute('''
            INSERT OR REPLACE INTO channels (channel_id, name, channel_desc, subscriber_count, video_count, view_count, playlist_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            channel_data["channel_id"],
            channel_data["name"],
            channel_data["channel_desc"],
            channel_data["subscriber_count"],
            channel_data["video_count"],
            channel_data["view_count"],
            channel_data["playlist_id"]
        ))

        # Save video data
        for video in video_data:
            cursor.execute('''
                INSERT OR REPLACE INTO videos (video_id, channel_id, video_name, video_desc, published_at,views, likes, comments, duration, thumbnail, caption) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                video["video_id"],
                video["channel_id"],
                video["video_name"],
                video["video_desc"],
                video["published_at"],
                video["views"],
                video["likes"],
                video["comments"],
                video["duration"],
                video["thumbnail"],
                video["caption"]
                
            ))

        # Save comment data
        for video_id, comments in comment_data.items():
            if not isinstance(comments, list):
                raise ValueError(f"Invalid comments data for video_id={video_id}. Expected a list, got {type(comments)}")

            for comment in comments:
                cursor.execute('''
                    INSERT INTO comments (comment_id, video_id, comment_text, author, comment_published_date) 
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    comment.get("comment_id"),
                    video_id,  # Use video_id from the dictionary key
                    comment.get("comment_text", ""),
                    comment.get("author", "Unknown"),
                    comment.get("comment_published_date", None)
                ))
        
        conn.commit()
        return {"duplicate_channel": None}  # No duplicates found
    except Exception as e:
        raise Exception(f"An error occurred while saving data: {e}")
    finally:
        conn.close()

def execute_query(query):
    """
    Executes a SQL query on the database and returns the result as a Pandas DataFrame.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def search_data(channel_name=None):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Specify unique column names for the joined query
    query = '''
        SELECT 
            channels.channel_id AS channel_id, 
            channels.name AS channel_name, 
            channels.subscriber_count, 
            channels.video_count, 
            channels.playlist_id,
            videos.video_id, 
            videos.likes, 
            videos.comments
        FROM channels 
        JOIN videos ON channels.channel_id = videos.channel_id
    '''
    params = ()
    if channel_name:
        query += " WHERE channels.name LIKE ?"
        params = (f'%{channel_name}%',)

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    # Define the unique column names for the DataFrame
    columns = ['channel_id', 'channel_name', 'subscriber_count', 'video_count', 'playlist_id', 
               'video_id', 'likes', 'comments']
    results_df = pd.DataFrame(results, columns=columns)
    return results_df
