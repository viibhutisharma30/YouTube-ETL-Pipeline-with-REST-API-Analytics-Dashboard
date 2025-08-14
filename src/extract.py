# src/extract.py
from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY, YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION

def get_youtube_service():
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)

def fetch_channel_details(channel_id):
    youtube = get_youtube_service()
    request = youtube.channels().list(part="snippet,statistics", id=channel_id)
    return request.execute()

def fetch_videos_by_channel(channel_id, max_results=50):
    youtube = get_youtube_service()
    # CORRECTED: Removed extra '()' after 'youtube'
    request = youtube.search().list(part="snippet", channelId=channel_id, maxResults=max_results, type='video')
    return request.execute()

# A new function in src/extract.py
def fetch_videos_by_topic(query, max_pages=3):
    youtube = get_youtube_service()
    all_videos = []
    next_page_token = None

    for _ in range(max_pages):
        request = youtube.search().list(
            q=query,
            part="snippet",
            maxResults=50,
            type='video',
            pageToken=next_page_token
        )
        response = request.execute()
        all_videos.extend(response.get('items', []))
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    
    return {"items": all_videos}


def fetch_comments(video_id):
    youtube = get_youtube_service()
    request = youtube.commentThreads().list(part="snippet", videoId=video_id, maxResults=100)
    return request.execute()

def fetch_video_details(video_ids):
    youtube = get_youtube_service()
    video_ids_str = ','.join(video_ids)
    # CORRECTED: Removed extra '()' after 'youtube'
    request = youtube.videos().list(part="snippet,statistics", id=video_ids_str)
    return request.execute()

def fetch_channel_details_batch(channel_ids):
    """
    Fetch details for multiple channels at once.
    channel_ids: list of channel IDs
    """
    youtube = get_youtube_service()
    channel_ids_str = ','.join(channel_ids)
    
    request = youtube.channels().list(
        part="snippet,statistics",
        id=channel_ids_str
    )
    return request.execute()


