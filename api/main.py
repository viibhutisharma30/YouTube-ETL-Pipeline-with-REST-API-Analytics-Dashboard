from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import pandas as pd
import os

app = FastAPI()

# Allow CORS for frontend (e.g., Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Corrected path to the database file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "database", "youtube.db"))

@app.get("/")
def root():
    return {"message": "YouTube ETL FastAPI is running!"}

@app.get("/channels/")
def get_channels():
    """Returns all channels from the database."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM channels", conn)
    conn.close()
    return df.to_dict(orient="records")

@app.get("/videos/")
def get_videos():
    """Returns all videos from the database."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM videos", conn)
    conn.close()
    return df.to_dict(orient="records")

@app.get("/comments/")
def get_comments():
    """Returns all comments from the database."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM comments", conn)
    conn.close()
    return df.to_dict(orient="records")

@app.get("/videos/top-views")
def get_top_videos(limit: int = 10):
    """Returns top videos by view count."""
    conn = sqlite3.connect(DB_PATH)
    # The 'viewCount' column must exist in the 'videos' table for this query to work.
    query = f"""
        SELECT title, viewCount, publishedAt
        FROM videos
        ORDER BY viewCount DESC
        LIMIT {limit}
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient="records")

@app.get("/channels/top-views")
def get_top_channels(limit: int = 10):
    """Returns top channels by view count."""
    conn = sqlite3.connect(DB_PATH)
    query = f"""
        SELECT title, viewCount
        FROM channels
        ORDER BY viewCount DESC
        LIMIT {limit}
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient="records")

@app.get("/summary")
# ... (rest of the code) ...

@app.get("/summary")
def get_summary():
    """Returns a summary of key statistics."""
    conn = sqlite3.connect(DB_PATH)
    
    # Calculate average views per channel
    channel_summary = pd.read_sql_query("SELECT AVG(viewCount) as avg_views FROM channels", conn)
    
    # Get total video and comment counts
    video_count = pd.read_sql_query("SELECT COUNT(*) as total_videos FROM videos", conn)
    comment_count = pd.read_sql_query("SELECT COUNT(*) as total_comments FROM comments", conn)
    
    conn.close()
    
    # Corrected: Explicitly convert NumPy types to Python types
    avg_channel_views = float(channel_summary['avg_views'].iloc[0]) if not channel_summary.empty else 0.0
    total_videos = int(video_count['total_videos'].iloc[0]) if not video_count.empty else 0
    total_comments = int(comment_count['total_comments'].iloc[0]) if not comment_count.empty else 0

    return {
        "average_channel_views": avg_channel_views,
        "total_videos": total_videos,
        "total_comments": total_comments
    }

# ... (rest of the code) ...

@app.get("/search")
def search_videos(q: str):
    """Search videos by keyword in the title."""
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT * FROM videos WHERE title LIKE ?
    """
    # Use parameterized query to prevent SQL injection
    df = pd.read_sql_query(query, conn, params=('%' + q + '%',))
    conn.close()
    return df.to_dict(orient="records")

@app.get("/videos/daily-uploads")
def daily_uploads():
    """Returns daily upload trends."""
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT DATE(publishedAt) AS day, COUNT(*) AS uploads
        FROM videos
        GROUP BY day
        ORDER BY day
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient="records")







