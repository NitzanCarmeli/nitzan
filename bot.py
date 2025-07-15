from flask import Flask, request
import requests
import tweepy
import os
from datetime import datetime, timezone

# Environment Variables
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
TWITTER_BEARER_TOKEN = os.environ['TWITTER_BEARER_TOKEN']
TWITTER_USERNAME = os.environ['TWITTER_USERNAME']

# Constants
START_DATE = datetime(2025, 7, 15, tzinfo=timezone.utc)
LAST_TWEET_FILE = "last_tweet_id.txt"

# Flask app for Render
app = Flask(__name__)

# Set up Twitter client
client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

def get_latest_tweet(username):
    user = client.get_user(username=username)
    tweets = client.get_users_tweets(
        id=user.data.id,
        max_results=5,
        tweet_fields=["created_at"]
    )

    if tweets.data:
        for tweet in tweets.data:
            if tweet.created_at > START_DATE:
                return tweet
    return None

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)

def get_last_sent_tweet_id():
    try:
        with open(LAST_TWEET_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_last_sent_tweet_id(tweet_id):
    with open(LAST_TWEET_FILE, "w") as f:
        f.write(str(tweet_id))

@app.route("/")
def run_bot():
    tweet = get_latest_tweet(TWITTER_USERNAME)
    if tweet:
        last_id = get_last_sent_tweet_id()
        if str(tweet.id) != last_id:
            send_to_telegram(tweet.text)
            save_last_sent_tweet_id(tweet.id)
            return "✅ Tweet sent"
        else:
            return "⏸ No new tweet"
    return "ℹ️ No tweet after start date"

if __name__ == "__main__":
    app.run()
