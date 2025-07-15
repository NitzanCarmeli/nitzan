import os
import requests
from datetime import datetime, timezone
from tweepy import Client

TWITTER_BEARER_TOKEN = os.environ['TWITTER_BEARER_TOKEN']
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
TWITTER_USERNAME = os.environ['TWITTER_USERNAME']

client = Client(bearer_token=TWITTER_BEARER_TOKEN)

# Set your start date here (only fetch tweets AFTER this date)
START_DATE = datetime(2025, 7, 1, tzinfo=timezone.utc)

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    requests.post(url, json=payload)

def send_photo_to_telegram(photo_url):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "photo": photo_url
    }
    requests.post(url, json=payload)

def send_video_to_telegram(video_url):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVideo"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "video": video_url
    }
    requests.post(url, json=payload)

def main():
    # Get user ID from username
    user = client.get_user(username=TWITTER_USERNAME)
    if user.data is None:
        print("User not found")
        return
    
    # Fetch tweets with media expansions
    tweets = client.get_users_tweets(
        id=user.data.id,
        max_results=5,
        tweet_fields=["created_at", "attachments", "text"],
        expansions=["attachments.media_keys"],
        media_fields=["url", "type"]
    )
    
    if tweets.data is None:
        print("No tweets found")
        return
    
    # Parse media info
    media = {}
    if tweets.includes and "media" in tweets.includes:
        for m in tweets.includes["media"]:
            media[m.media_key] = m
    
   for tweet in tweets.data:
    if tweet.created_at > START_DATE:
        tweet_url = f"https://twitter.com/{TWITTER_USERNAME}/status/{tweet.id}"

        # שלח רק את הקישור לציוץ (בלי הטקסט)
        message = f"<a href='{tweet_url}'>לצפייה בציוץ בטוויטר</a>"
        send_to_telegram(message)

        # מדיה? נשלח בנפרד
        if hasattr(tweet, 'attachments') and 'media_keys' in tweet.attachments:
            for media_key in tweet.attachments['media_keys']:
                m = media.get(media_key)
                if m:
                    if m.type == "photo":
                        send_photo_to_telegram(m.url)
                    elif m.type in ["video", "animated_gif"]:
                        # רק נשלח את הקישור ולא ננסה לשלוח את הווידאו
                        send_to_telegram(f"<a href='{tweet_url}'>לצפייה בסרטון בטוויטר</a>")


if __name__ == "__main__":
    main()
