import streamlit as st 
import pandas as pd
import requests
import altair as alt
from textblob import TextBlob

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="📊 YouTube ETL Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 YouTube ETL Dashboard")

# --- Function to Load Data from FastAPI Backend ---
@st.cache_data(ttl=60)
def load_data():
    """Fetches data from FastAPI endpoints."""
    base_url = "http://127.0.0.1:8000"

    try:
        channels = pd.DataFrame(requests.get(f"{base_url}/channels/").json())
        videos = pd.DataFrame(requests.get(f"{base_url}/videos/").json())
        comments = pd.DataFrame(requests.get(f"{base_url}/comments/").json())
        summary = requests.get(f"{base_url}/summary").json()
        return channels, videos, comments, summary

    except requests.exceptions.ConnectionError:
        st.error("⚠️ FastAPI server not reachable. Please start your backend.")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), {}
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), {}

# --- Load Data ---
channels_df, videos_df, comments_df, summary_data = load_data()

# --- Data Preprocessing ---
if not videos_df.empty:
    videos_df["publishedAt"] = pd.to_datetime(videos_df["publishedAt"], errors='coerce')
    videos_df["viewCount"] = pd.to_numeric(videos_df["viewCount"], errors='coerce')
    videos_df.dropna(subset=["publishedAt", "viewCount"], inplace=True)

# 1️⃣ Overall Statistics
st.header("📈 Overall Statistics")
if summary_data:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Videos Extracted", summary_data.get("total_videos", "N/A"))
    col2.metric("Total Comments Extracted", summary_data.get("total_comments", "N/A"))
    col3.metric("Avg Channel Views", f"{summary_data.get('average_channel_views', 0):,.0f}")
else:
    st.info("No summary data available.")

# 2️⃣ Daily Video Upload Trends
st.header("📅 Daily Video Upload Trends")
if not videos_df.empty:
    daily_uploads = videos_df.groupby(videos_df["publishedAt"].dt.date).size().reset_index(name="Upload Count")
    daily_uploads.columns = ["Date", "Upload Count"]
    line_chart = alt.Chart(daily_uploads).mark_line(point=True).encode(
        x="Date:T", y="Upload Count:Q", tooltip=["Date", "Upload Count"]
    ).interactive()
    st.altair_chart(line_chart, use_container_width=True)
else:
    st.info("No video data for trends.")

# 3️⃣ Top 10 Videos by View Count
st.header("🔥 Top 10 Videos by View Count")
if not videos_df.empty:
    top_videos = videos_df.sort_values(by="viewCount", ascending=False).head(10)
    bar_chart = alt.Chart(top_videos).mark_bar().encode(
        x="viewCount:Q",
        y=alt.Y("title:N", sort='-x'),
        tooltip=["title", "viewCount", "publishedAt"]
    ).interactive()
    st.altair_chart(bar_chart, use_container_width=True)
else:
    st.info("No video data to show top videos.")

# 4️⃣ Video Category Distribution
st.header("📊 Video Category Distribution")
if not videos_df.empty and "category_id" in videos_df.columns:
    category_counts = videos_df["category_id"].value_counts().reset_index(name="Video Count")
    category_counts.columns = ["Category ID", "Video Count"]
    pie_chart = alt.Chart(category_counts).mark_arc().encode(
        theta="Video Count",
        color="Category ID:N",
        tooltip=["Category ID", "Video Count"]
    )
    st.altair_chart(pie_chart, use_container_width=True)
else:
    st.info("No category data found.")

# 5️⃣ Filterable Video List
st.header("📋 Filterable Video List")
if not videos_df.empty:
    st.sidebar.header("Video Filters")
    search_query = st.sidebar.text_input("Search by Title", "")
    if 'topic' in videos_df.columns:
        topics = ["All"] + sorted(list(videos_df["topic"].unique()))
        selected_topic = st.sidebar.selectbox("Filter by Topic", topics)
    else:
        selected_topic = "All"
    min_views, max_views = int(videos_df["viewCount"].min()), int(videos_df["viewCount"].max())
    view_range = st.sidebar.slider("View Count Range", min_views, max_views, (min_views, max_views))

    filtered_videos = videos_df.copy()
    if search_query:
        filtered_videos = filtered_videos[filtered_videos["title"].str.contains(search_query, case=False, na=False)]
    if selected_topic != "All":
        filtered_videos = filtered_videos[filtered_videos["topic"] == selected_topic]
    filtered_videos = filtered_videos[
        (filtered_videos["viewCount"] >= view_range[0]) & 
        (filtered_videos["viewCount"] <= view_range[1])
    ]
    st.dataframe(filtered_videos[["title", "viewCount", "publishedAt", "topic", "category_id"]])
else:
    st.info("No video data to filter.")

# 6️⃣ Comment Sentiment Analysis
st.header("💬 Comment Sentiment Analysis")
if not comments_df.empty and "text" in comments_df.columns:
    comments_df["sentiment_score"] = comments_df["text"].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
    def label_sentiment(score):
        if score > 0.05:
            return "Positive"
        elif score < -0.05:
            return "Negative"
        return "Neutral"
    comments_df["sentiment_label"] = comments_df["sentiment_score"].apply(label_sentiment)
    sentiment_counts = comments_df["sentiment_label"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]
    sentiment_chart = alt.Chart(sentiment_counts).mark_bar().encode(
        x="Sentiment:N", y="Count:Q", color="Sentiment"
    )
    st.altair_chart(sentiment_chart, use_container_width=True)
    avg_sentiment_per_video = comments_df.groupby("video_id")["sentiment_score"].mean().reset_index()
    avg_sentiment_per_video.columns = ["Video ID", "Average Sentiment Score"]
    st.subheader("📊 Average Sentiment per Video")
    st.dataframe(avg_sentiment_per_video)
else:
    st.info("No comments available for sentiment analysis.")

# 7️⃣ Raw DataFrames
with st.expander("📂 View Raw DataFrames"):
    st.subheader("Channels Data")
    st.dataframe(channels_df)
    st.subheader("Videos Data")
    st.dataframe(videos_df)
    st.subheader("Comments Data")
    st.dataframe(comments_df)
