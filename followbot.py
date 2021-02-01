import tweepy
from tweepy import OAuthHandler
import config as config
from config import Common as c
import time
from datetime import datetime, timedelta
from time import sleep
import random

name = "username123"
Hours = 5 

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

#used to delete tweets from user acct	
def del_tweets(api, username):
    page = 1
    deadend = False
    tweets = api.user_timeline(username, page = page)

    for i,tweet in enumerate(tweets):
        if datetime.now()-timedelta(hours=Hours) <= tweet.created_at:
            print(f'Removed \'{tweet.text}\'')
            api.destroy_status(tweet.id)
            sleep(0.5)
        else:
            deadend = True
            return
    if not deadend:
        page+=1
        time.sleep(10)

# search for tweets with specific keywords - static 
def searchNode(api):
	#add random word selector from dict file
	filename = "googletxt.txt"
	candidates = [x.strip().lower() for x in open(filename,"r")]
	followcount = 0 #initfollowcounnt
	while(filename):
		word = candidates[(random.randint(0,len(candidates) - 1))]
		print('word: ' + word)
		for tweet in api.search(q = word, count = 1):
			print(f"{tweet.user.name}:{tweet.text}")
			time.sleep(4)
			if tweet.favorite_count > 20: #make sure has < 20 faves
				if not tweet.retweeted: #check if already retweeted
					try:
						tweet.retweet()
						tweet.favorite()
					except Exception as e:
						print("error on retweet/fav\n")
			if followcount < 750:	# cap follow at 750/day to avoid ban
				if tweet.user.followers_count > 100: #worthwhile follow - i think
					try: 
						if tweet.user.follow():
							followcount+=1
					except Exception as e:
						print("error on follow\n")
			else:
				print("Daily follow limit reached!")

#steam listener class 				
class MyStreamListener(tweepy.StreamListener):
	#init
	def on_status(self, data):
		self.process(data)
		return True
		
	#listener functionality
	def process(self, data):
		print(data.text)
		#if data.user.follow():
			#print("followed")
		sleep(2)
		
	def on_error(self, data):
		if status_code == 420:
			return False
		print(data.text)

def CreateStream(api, listener):
	myStreamListener = MyStreamListener()
	s = tweepy.Stream(auth = api.auth, listener=myStreamListener)
	s.filter(track=['Follow']) #set track
	sleep(1)
	
if __name__ == "__main__":
	api = main() #get auth
	#listener = MyStreamListener() #create listener
	#CreateStream(api, listener)
	qlist = ['Crypto','Politics','Sports','Food','Trump','Biden']  #custom tag list
	#for i in qlist:
	searchNode(api)