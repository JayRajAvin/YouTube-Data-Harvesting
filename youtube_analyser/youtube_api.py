from googleapiclient.discovery import build
import streamlit as st
import isodate
from datetime import datetime

# Set up Google API for YouTube
API_KEY = 'AIzaSyAZUSH-41RJ5-MVSTO7kv1sr_rOA7SwqAA'
youtube = build('youtube', 'v3', developerKey=API_KEY)

def retrieve_youtube_data(channel_id):
    # Fetch channel details
    channel_request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id
    )
    channel_response = channel_request.execute()

    # Ensure the response contains data
    if not channel_response.get('items'):
        raise ValueError("No channel data found. Please check the Channel ID.")

    channel_info = channel_response['items'][0]
    channel_data = {
        "channel_id": channel_id,
        "name": channel_info['snippet']['title'],
        "channel_desc": channel_info['snippet']['description'],
        "subscriber_count": int(channel_info['statistics']['subscriberCount']),
        "video_count": int(channel_info['statistics']['videoCount']),
        "view_count": int(channel_info['statistics']['viewCount']),
        "playlist_id": channel_info['contentDetails']['relatedPlaylists']['uploads']
    }

    # Fetch video details from playlist
    video_data = []
    comment_data = {}  # Change from list to dictionary
    playlist_id = channel_data['playlist_id']
    playlist_request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=20  
    )
    playlist_response = playlist_request.execute()

    # Ensure the playlist contains videos
    if not playlist_response.get('items'):
        st.warning("No videos found in the playlist.")
        return channel_data, video_data, comment_data

    for item in playlist_response['items']:
        video_id = item['snippet']['resourceId'].get('videoId')
        if not video_id:
            continue  # Skip if videoId is missing

        video_request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        video_response = video_request.execute()

        if not video_response.get('items'):
            continue  # Skip if video details are missing

        video_info = video_response['items'][0]
        #Parse duration
        duration_iso = video_info['contentDetails']['duration']
        duration_seconds = int(isodate.parse_duration(duration_iso).total_seconds()) 

        published_at_iso = video_info['snippet']['publishedAt']
        published_at = datetime.strptime(published_at_iso, "%Y-%m-%dT%H:%M:%SZ") 
        published_at_formatted = published_at.strftime("%B %d, %Y, %I:%M %p")      

        video_data.append({
            "video_id": video_id,
            "channel_id": channel_id,
            "video_name": video_info['snippet']['title'] if 'title' in video_info['snippet'] else "Not Available",
            "video_desc": video_info['snippet']['description'],
            "views": int(video_info['statistics'].get('viewCount', 0)),
            "likes": int(video_info['statistics'].get('likeCount', 0)),
            "comments": int(video_info['statistics'].get('commentCount', 0)),
            "published_at": video_info['snippet']['publishedAt'],
            "duration": duration_seconds,
            "thumbnail": video_info['snippet']['thumbnails']['high']['url'],
            "caption": video_info['contentDetails']['caption'],
        })

        # Fetch top-level comments for the video
        comment_data[video_id] = []  # Initialize the list for this video_id
        comment_request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100  # Fetch up to 100 comments per video
        )
        comment_response = comment_request.execute()

        if comment_response.get('items'):
            for comment in comment_response['items']:
                snippet = comment['snippet']['topLevelComment']['snippet']
                comment_data[video_id].append({
                    "comment_id": comment['id'],
                    "text": snippet['textDisplay'],
                    "author": snippet['authorDisplayName'],                    
                    "comment_published_date": snippet['publishedAt']
                })

    return channel_data, video_data, comment_data

