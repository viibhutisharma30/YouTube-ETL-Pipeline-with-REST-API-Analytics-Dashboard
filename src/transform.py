# # src/transform.py
# import pandas as pd


# def transform_channel_data(raw):
#     items = raw.get("items", [])
#     return [{
#         "channel_id": item["id"],
#         "title": item["snippet"]["title"],
#         "description": item["snippet"]["description"],
#         "viewCount": item["statistics"]["viewCount"]
#     } for item in items]

# def transform_video_data(raw):
#     items = raw.get("items", [])
#     transformed_data = []
#     for item in items:
#         snippet = item.get("snippet", {})
#         statistics = item.get("statistics", {})

#         video_info = {
#             "video_id": item.get("id"),
#             "title": snippet.get("title"),
#             "publishedAt": snippet.get("publishedAt"),
#             "viewCount": int(statistics.get("viewCount", 0)) if statistics.get("viewCount") else None,
#             "category_id": snippet.get("categoryId"),
#             "channel_id": snippet.get("channelId"),
#             "channelTitle": snippet.get("channelTitle")
#         }
#         transformed_data.append(video_info)
#     return transformed_data


# def transform_comments_data(raw):
#     items = raw.get("items", [])
#     return [{
#         "comment_id": item["id"],
#         "video_id": item["snippet"]["topLevelComment"]["snippet"]["videoId"],
#         "text": item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
#     } for item in items]

# def transform_channel_data_batch(raw):
#     items = raw.get("items", [])
#     return [{
#         "channel_id": item["id"],
#         "title": item["snippet"]["title"],
#         "description": item["snippet"]["description"],
#         "viewCount": item["statistics"]["viewCount"]
#     } for item in items]


# src/transform.py
import pandas as pd
from textblob import TextBlob  # For sentiment analysis


def transform_channel_data(raw):
    items = raw.get("items", [])
    return [{
        "channel_id": item["id"],
        "title": item["snippet"]["title"],
        "description": item["snippet"]["description"],
        "viewCount": int(item["statistics"]["viewCount"]) if item["statistics"].get("viewCount") else 0
    } for item in items]


def transform_video_data(raw):
    items = raw.get("items", [])
    transformed_data = []
    for item in items:
        snippet = item.get("snippet", {})
        statistics = item.get("statistics", {})

        video_info = {
            "video_id": item.get("id"),
            "title": snippet.get("title"),
            "publishedAt": snippet.get("publishedAt"),
            "viewCount": int(statistics.get("viewCount", 0)) if statistics.get("viewCount") else None,
            "category_id": snippet.get("categoryId"),
            "channel_id": snippet.get("channelId"),
            "channelTitle": snippet.get("channelTitle")
        }
        transformed_data.append(video_info)
    return transformed_data


def transform_comments_data(raw):
    items = raw.get("items", [])
    comments_data = []

    for item in items:
        comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        sentiment_score = TextBlob(str(comment_text)).sentiment.polarity

        # Classify as Positive, Neutral, or Negative
        if sentiment_score > 0:
            sentiment_label = "Positive"
        elif sentiment_score < 0:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Neutral"

        comments_data.append({
            "comment_id": item["id"],
            "video_id": item["snippet"]["topLevelComment"]["snippet"]["videoId"],
            "text": comment_text,
            "sentiment_score": sentiment_score,
            "sentiment_label": sentiment_label
        })

    return comments_data


def transform_channel_data_batch(raw):
    items = raw.get("items", [])
    return [{
        "channel_id": item["id"],
        "title": item["snippet"]["title"],
        "description": item["snippet"]["description"],
        "viewCount": int(item["statistics"]["viewCount"]) if item["statistics"].get("viewCount") else 0
    } for item in items]
