# src/run_elt.py
from extract import fetch_videos_by_topic, fetch_video_details, fetch_comments, fetch_channel_details_batch
from transform import transform_video_data, transform_comments_data, transform_channel_data_batch
from load import load_to_db
import os

# Define the topics you want to analyze
topics = ["Data Engineering"]

def run_etl(topics_list):
    all_channel_ids = set() 
    
    for topic in topics_list:
        print(f"\nProcessing topic: {topic}")
        
        # 1. Extract videos for the topic (with pagination)
        raw_video_search_data = fetch_videos_by_topic(topic, max_pages=3)
        video_ids = [item["id"]["videoId"] for item in raw_video_search_data.get("items", []) if item["id"].get("videoId")]
        print(f"  Found {len(video_ids)} videos to process.")
        
        # 2. Get detailed video info and comments
        raw_video_details_data_list = []
        for i in range(0, len(video_ids), 50):
            batch_video_ids = video_ids[i:i + 50]
            print(f"  Fetching details for batch of {len(batch_video_ids)} videos...")
            
            try:
                raw_video_details_data = fetch_video_details(batch_video_ids)
                raw_video_details_data_list.append(raw_video_details_data)
            except Exception as e:
                print(f"  Could not fetch video details for a batch: {e}")
                continue
        
        all_videos_items = []
        for batch in raw_video_details_data_list:
            all_videos_items.extend(batch.get("items", []))
            
        for item in all_videos_items:
            channel_id = item["snippet"]["channelId"]
            all_channel_ids.add(channel_id)
        
        raw_comments_data = []
        print("  Fetching comments...")
        for vid in video_ids:
            try:
                comment_data = fetch_comments(vid)
                raw_comments_data.extend(comment_data.get("items", []))
            except Exception as e:
                print(f"  Could not fetch comments for video {vid}: {e}")
                continue

        # 3. Transform and Load
        print("  Transforming and Loading data...")
        videos = transform_video_data({"items": all_videos_items})
        comments = transform_comments_data({"items": raw_comments_data})

        for video in videos:
            video['topic'] = topic

        load_to_db(videos, "videos")
        load_to_db(comments, "comments")
    
    # --- CRITICAL FIX: Ensure channel data is fetched and loaded ---
    if all_channel_ids:
        print("\nFetching and loading channel data for discovered channels...")
        # Split channel IDs into batches of 50 for the API call
        channel_ids_list = list(all_channel_ids)
        for i in range(0, len(channel_ids_list), 50):
            batch_channel_ids = channel_ids_list[i:i + 50]
            try:
                raw_channel_data = fetch_channel_details_batch(batch_channel_ids)
                channels = transform_channel_data_batch(raw_channel_data)
                load_to_db(channels, "channels")
            except Exception as e:
                print(f"  Could not fetch channel details for a batch: {e}")
                continue
    # --- FIX ENDS HERE ---

    print("\nETL pipeline completed successfully for all topics.")

if __name__ == "__main__":
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "database", "youtube.db")
    if os.path.exists(db_path):
        os.remove(db_path)
    
    run_etl(topics)