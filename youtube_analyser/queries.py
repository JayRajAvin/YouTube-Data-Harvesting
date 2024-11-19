def get_video_names_and_channels():
    """
    Query to get video names and their corresponding channel names.
    """
    return '''
        SELECT videos.video_name AS video_name, channels.name AS channel_name
        FROM videos
        JOIN channels ON videos.channel_id = channels.channel_id;
    '''

def get_channels_with_most_videos():
    """
    Query to get channels with the most videos.
    """
    return '''
        SELECT channels.name AS channel_name, COUNT(videos.video_id) AS video_count
        FROM videos
        JOIN channels ON videos.channel_id = channels.channel_id
        GROUP BY channels.channel_id
        ORDER BY video_count DESC;
    '''

# Query for top 10 most viewed videos
def get_top_10_most_viewed_videos():
    return """
    SELECT 
        videos.video_name AS video_name, 
        channels.name AS channel_name, 
        videos.views AS view_count
    FROM 
        videos
    JOIN 
        channels 
    ON 
        videos.channel_id = channels.channel_id
    ORDER BY 
        videos.views DESC
    LIMIT 10;
    """
# Query for the number of comments on each video
def get_video_comment_counts():
    return """
    SELECT 
        videos.video_name AS video_name, 
        COUNT(comments.comment_id) AS comment_count
    FROM 
        videos
    LEFT JOIN 
        comments 
    ON 
        videos.video_id = comments.video_id
    GROUP BY 
        videos.video_id, videos.video_name
    ORDER BY 
        comment_count DESC;
    """
# Query for videos with the highest likes and corresponding channel names
def get_videos_with_highest_likes():
    return """
    SELECT 
        videos.video_name AS video_name, 
        channels.name AS channel_name, 
        videos.likes AS like_count
    FROM 
        videos
    JOIN 
        channels 
    ON 
        videos.channel_id = channels.channel_id
    ORDER BY 
        videos.likes DESC;
    """
# Query for total likes and dislikes for each video with video names
def get_total_likes_per_video():
    return """
    SELECT 
        videos.video_name AS video_name, 
        videos.likes AS total_likes
    FROM 
        videos
    ORDER BY 
        videos.likes DESC;
    """
# Query for total views for each channel with their names
def get_total_views_per_channel():
    return """
    SELECT 
        channels.name AS channel_name, 
        SUM(videos.views) AS total_views
    FROM 
        videos
    JOIN 
        channels 
    ON 
        videos.channel_id = channels.channel_id
    GROUP BY 
        channels.name
    ORDER BY 
        total_views DESC;
    """
# Query for channels that published videos in 2022
def get_channels_with_videos_in_2022():
    return """
    SELECT DISTINCT 
        channels.name AS channel_name
    FROM 
        videos
    JOIN 
        channels 
    ON 
        videos.channel_id = channels.channel_id
    WHERE 
        substr(videos.published_at, 1, 4) = '2024';
    """
# Query for average video duration per channel
def get_average_video_duration_per_channel():
    return """
    SELECT 
        channels.name AS channel_name,
        AVG(videos.duration) / 60.0 AS average_duration_minutes
    FROM 
        videos
    JOIN 
        channels 
    ON 
        videos.channel_id = channels.channel_id
    GROUP BY 
        channels.channel_id;
    """
# Query for videos with the highest number of comments
def get_video_with_highest_comments():
    return """
    SELECT 
        videos.video_name, 
        channels.name AS channel_name,
        videos.comments AS comment_count
    FROM 
        videos
    JOIN 
        channels 
    ON 
        videos.channel_id = channels.channel_id
    ORDER BY 
        videos.comments DESC
    LIMIT 1;
    """



