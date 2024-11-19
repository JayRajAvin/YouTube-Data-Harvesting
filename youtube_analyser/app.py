import streamlit as st
from youtube_api import retrieve_youtube_data
from database import create_tables, save_data_to_database, execute_query, search_data
from queries import get_video_names_and_channels, get_channels_with_most_videos, get_top_10_most_viewed_videos 
from queries import get_video_comment_counts, get_videos_with_highest_likes, get_total_likes_per_video
from queries import get_total_views_per_channel, get_channels_with_videos_in_2022, get_average_video_duration_per_channel, get_video_with_highest_comments
import json

def load_css(file_name):
    with open(file_name, "r") as css_file:
        st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

# Load CSS file
load_css("styles.css")

# Initialize database tables
create_tables()

# App UI
st.title("YouTube Data Harvesting")

# Session state to store retrieved data
if 'channel_data' not in st.session_state:
    st.session_state['channel_data'] = None
if 'video_data' not in st.session_state:
    st.session_state['video_data'] = None
if 'comment_data' not in st.session_state:
    st.session_state['comment_data'] = None

# Sidebar Menu with Icons
menu = {
    "Home": "🏠",
    "Json - Retrieve Channel Data": "📊",
    "Non-Json - Retrieve Channel Data": "📊",
    "Retrieve by Channel Name": "🔍",
    "SQL Query Output": "🔍",
    
}
choice = st.sidebar.selectbox("**Select an option**", list(menu.keys()), format_func=lambda x: f"{menu[x]} {x}")

# Home Page
if choice == "Home":
    st.write("""
        Welcome to the **YouTube Data Harvesting and Warehousing using SQL and Streamlit**. 
        Use this app to retrieve data from YouTube channels and view comments and video statistics.
    """)

# Retrieve YouTube Data
elif choice == "Json - Retrieve Channel Data":
    # Input for Channel ID
    channel_id = st.text_input("**Enter YouTube Channel ID**")

    # Button layout
    col1, col2 = st.columns(2)
    with col1:
        retrieve_button_clicked = st.button("Json Retrieve Channel Data")
    with col2:
        save_button_clicked = st.button("Save Data to Database")

    # Placeholder for JSON output
    json_placeholder = st.empty()

    # Button to retrieve data in JSON format
    if retrieve_button_clicked:
        if channel_id:
            with st.spinner('Retrieving data from YouTube...'):
                try:
                    # Fetch data
                    channel_data, video_data, comment_data = retrieve_youtube_data(channel_id)
                    st.session_state['channel_data'] = channel_data
                    st.session_state['video_data'] = video_data
                    st.session_state['comment_data'] = comment_data

                    
                    # Combine all data into a hierarchical JSON structure
                    json_output = {
                        "channel": {
                            "name": channel_data["name"],
                            "channel_id": channel_data["channel_id"],
                            "subscriber_count": channel_data["subscriber_count"],
                            "video_count": channel_data["video_count"],
                            "view_count": channel_data["view_count"],
                            "channel_desc": channel_data["channel_desc"],
                            "playlist_id": channel_data['playlist_id'],
                            "videos": []
                        }
                    }

                    # Add videos and their comments to the JSON
                    for video in video_data:
                        video_entry = {
                            "video_id": video["video_id"],
                            "title": video.get("video_name", "Unknown"),
                            "video_desc": video.get("video_desc", ""),
                            "views": video.get("views", 0),
                            "likes": video.get("likes", 0),
                            "comments_count": video.get("comments", 0),
                            "published_at": video.get("published_at", ""),
                            "duration": video.get("duration", ""),
                            "comments": comment_data.get(video["video_id"], [])
                        }
                        json_output["channel"]["videos"].append(video_entry)

                    # Display the JSON in the app
                    json_placeholder.write("Hierarchical JSON Representation:")
                    json_placeholder.json(json_output)
                    

                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a valid Channel ID")
    
    # Save Data to Database
    if save_button_clicked:
        if st.session_state['channel_data'] and st.session_state['video_data'] and st.session_state['comment_data']:
            with st.spinner('Saving data to the database...'):
                try:
                    # Call the function to save data
                    result = save_data_to_database(
                        st.session_state['channel_data'], 
                        st.session_state['video_data'], 
                        st.session_state['comment_data']
                    )
                    if result["duplicate_channel"]:
                        st.warning(f"Channel with ID '{result['duplicate_channel']}' already exists in the database. No new data was saved.")
                    else:
                        st.success("Data saved to database successfully!")

                     # Reset states after saving
                    st.session_state['channel_data'] = None
                    st.session_state['video_data'] = None
                    st.session_state['comment_data'] = None
                    
                except Exception as e:
                    st.error(f"An error occurred while saving data: {e}")
        else:
            st.warning("No data to save. Retrieve channel data first.")
        
elif choice == "Non-Json - Retrieve Channel Data":
    # Input for Channel ID
    channel_id = st.text_input("**Enter YouTube Channel ID**")

    # Button to retrieve data
    if st.button("Retrieve Channel Data"):
        with st.spinner('Retrieving data from YouTube...'):
            if channel_id:
                try:
                    # Fetch data
                    channel_data, video_data, comment_data = retrieve_youtube_data(channel_id)

                    # Display channel data
                    st.header(f"Channel: {channel_data['name']}")
                    st.subheader(f"Subscribers: {channel_data['subscriber_count']}")
                    st.subheader(f"Total Videos: {channel_data['video_count']}")

                    # Display videos and associated comments
                    for video in video_data:
                        with st.expander(f"Video: {video.get('video_name', 'Unknown')} (Likes: {video.get('likes', 0)}, Comments: {video.get('comments', 0)})"):
                            st.write(f"Video ID: {video['video_id']}")
                            st.write(f"Views: {video.get('views', 0)}")
                            st.write(f"Published At: {video.get('published_at', 'N/A')}")
                            st.write("Comments:")

                            video_comments = comment_data.get(video["video_id"], [])
                            if video_comments:
                                for comment in video_comments:
                                    st.markdown(f"- **{comment.get('author', 'Anonymous')}**: {comment.get('text', 'No Text')} (Published: {comment.get('published_at', 'N/A')})")
                            else:
                                st.write("No comments available for this video.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.warning("Please enter a valid Channel ID")

# Search Data
elif choice == "SQL Query Output":
    st.header("SQL Query Output")

    # Dropdown for query selection
    query_options = {
        "----  Select from the list  ----": None,  # Default option with no associated query
        "Video Names and Corresponding Channels": get_video_names_and_channels,
        "Channels with the Most Videos": get_channels_with_most_videos,
        "Top 10 Most Viewed Videos": get_top_10_most_viewed_videos,
        "Comment Count for Each Video": get_video_comment_counts,
        "Videos with Highest Likes and Channel Names": get_videos_with_highest_likes,
        "Total Likes per Video": get_total_likes_per_video,
        "Total Views per Channel": get_total_views_per_channel,
        "Channels with Videos in 2022": get_channels_with_videos_in_2022,
        "Average Video Duration per Channel": get_average_video_duration_per_channel,
        "Videos with Highest Comments": get_video_with_highest_comments
    }
    selected_query = st.selectbox("**Select a query to execute**", list(query_options.keys()))

    # Execute the selected query
    if selected_query == "----  Select from the list  ----":
        st.info("Please select a query to execute.")
    else:
        query_function = query_options[selected_query]
        query = query_function()
        result = execute_query(query)
        st.subheader(f"Results for: {selected_query}")
        st.write(result)

# Search Data
elif choice == "Retrieve by Channel Name":
    search_term = st.text_input("**Search Channel Name**")
    if st.button("Search"):
        results = search_data(channel_name=search_term)
        st.write("Search Results:")
        if len(results) > 0:
            st.dataframe(results)
        else:
            st.warning("No results found.")



    
        
    