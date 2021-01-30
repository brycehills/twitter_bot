import tweepy
from tweepy import OAuthHandler
import config as config
from config import Common as c
import time, datetime

def main():
	consumer_key=c.consumer_key
	consumer_secret=c.consumer_secret
	access_token=c.access_token
	access_token_secret=c.access_token_secret
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)
	return api
		
def searchNode(api):
	for tweet in api.search(q="x", count = 1000000000):
		print(f"{tweet.user.name}:{tweet.text}")
		if not tweet.retweeted:
			try:
				tweet.retweet()
			except Exception as e:
				print("error on retweet\n")
		if not tweet.user.follow():
			try: 
				tweet.user.follow()
			except Exception as e:
				print("error on follow\n")
			
def printFavorites(api):
	user_tweets = api.user_timeline('roman37416126', count=count)
	print(user_tweets)
	
if __name__ == "__main__":
	api = main()
	searchNode(api)
