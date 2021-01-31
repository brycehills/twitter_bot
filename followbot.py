import tweepy,json
from tweepy import OAuthHandler
import config as config
from config import Common as c
import time
from datetime import datetime, timedelta
from time import sleep

name = "roman37416126"
Hours = 5 

qlist = ['Stafford','Rams','Lions','coffee','korea','kpop','mask','wallstreetbets','covid','trump','twitter','github','follow','GME','bitcoin','google','facebook','california','Robinhood','AOC','TRX','Apple','AMC','Tesla','GE','Microsoft','Oracle','Nokia','Amazon','Democrat','Republican','American','Bank','Intel','AMD','Melvin','Uber','a', 'AAA', 'AAAS', 'aardvark', 'Aarhus', 'Aaron', 'ABA', 'Ababa','aback', 'abacus', 'abalone', 'abandon', 'abase', 'abash', 'abate','abbas', 'abbe', 'abbey', 'abbot', 'Abbott', 'abbreviate',"python", "jumble", "easy", "difficult", "answer", "xylophone"]

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
        time.sleep(20)
		
def searchNode(api,qitem):
	followcount = 0
	for tweet in api.search(q = qitem, count = 10):
		#print(f"{tweet.user.name}:{tweet.text}")
		time.sleep(5)
		if not tweet.retweeted:
			try:
				tweet.retweet()
				tweet.favorite()
			except Exception as e:
				print("error on retweet\n")
		if followcount < 100:
			try: 
				#tweet.user.follow()
				followcount+=1
			except Exception as e:
				print("error on follow\n")
			
def printFavorites(api):
	user_tweets = api.user_timeline('roman37416126', count=count)
	print(user_tweets)
	
if __name__ == "__main__":
	api = main()
	#del_tweets(api, name)
	for i in qlist:
		searchNode(api,i)
