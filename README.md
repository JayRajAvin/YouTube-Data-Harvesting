YouTube Data Harvesting and Warehousing using SQL and Streamlit

Overview
This Project is a Streamlit-based web application that integrates with the YouTube Data API to retrieve and analyze YouTube channel and video data. This application allows users to fetch detailed channel and video statistics, save them into a SQLite database, and perform insightful queries to explore patterns and trends.

Features
•	Retrieve YouTube channel details, including subscriber count, video count, view count, and more.
•	Fetch video-specific data, such as video titles, descriptions, views, likes, comments, and durations.
•	Save the retrieved data into a structured SQLite database.
•	Prevent duplicate channel entries in the database.
•	Perform various analytical SQL queries on the database, such as:
  o	Top 10 most viewed videos with their corresponding channels.
  o	Videos with the highest number of likes and their channel names …etc..
•	Display query results as interactive tables within the Streamlit app.
•	Handle exceptions gracefully, with meaningful error messages for better user experience.

Installation

Prerequisites
1.	Python 3.7 or higher
2.	A valid Google API Key with access to the YouTube Data API.
3.	Visual Studio Code(IDE)

Steps
1.	Clone this repository
2.	Navigate to the project directory
3.	Install the required dependencies:
    pip install -r requirements.txt

Usage

Running the Application
1.	Start the Streamlit app:
    streamlit run app.py
2.	Open the app in your browser at http://localhost:8501

Using the Application
1.	Retrieve Channel Data:
    o	Enter a valid YouTube Channel ID.
    o	Click the "Retrieve Data" button to fetch the channel's details, video data, and comments.
2.	Save Data:
    o	Once data is fetched, click "Save to Database" to store it in the SQLite database.
    o	If duplicate channel data is detected, an appropriate message will be displayed.
3.	Analyze Data:
    o	Select a query from the dropdown menu in the "SQL Query Output" section.
    o	View query results displayed in an interactive table.

File Dependency Flow
1.	app.py:
    o	Uses youtube_api.py to fetch data.
    o	Saves data using database.py.
    o	Runs queries from queries.py.
    o	Applies styles from style.css.
2.	youtube_api.py:
    o	Communicates with the YouTube Data API.
    o	Returns structured data to app.py.
3.	database.py:
    o	Manages database interactions.
    o	Provides data to app.py based on queries.
4.	queries.py:
    o	Supplies SQL queries for database.py.
5.	style.css:
    o	Modifies the appearance of components in app.py.

Database Schema
The SQLite database consists of three tables:
1. channels: Which contains all channels related details like channel_id, name and so on.
2. videos: Which contains all videos related details like video_id, video_name and so on.
3. videos: Which contains all comments related details like comment_id, author and so on.




