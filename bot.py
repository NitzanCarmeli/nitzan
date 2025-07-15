import tweepy
import requests


bearer_token = 'AAAAAAAAAAAAAAAAAAAAAEtI3AEAAAAAxZmjOPWsBTR3SjSgDVIMY7Rkqog%3DKmyvCPzbAl1ATswA9kL0iqnF2pxwDyfQNYDBPsVfDp45ANzlUH'

client = tweepy.Client(bearer_token=bearer_token)


telegram_token = '7922467459:AAFAiu3MSr7rPw9c1Igesj9h3TV-j7pPLtA'
telegram_chat_id = '@יערה זרד - Yaara Zered'


twitter_username = "YaaraZered"

def get_latest_tweet(username):
    user = client.get_user(username=username)
    tweets = client.get_users_tweets(id=user.data.id, max_results=5)
    if tweets.data:
        return tweets.data[0].text
    return None

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    data = {
        "chat_id": telegram_chat_id,
        "text": text
    }
    requests.post(url, data=data)


tweet = get_latest_tweet(twitter_username)
if tweet:
    send_to_telegram(tweet)
