import tweepy
from tweepy import TweepError, RateLimitError
import time #for sleep time
import credentials #for developer's tweeter credentials

auth = tweepy.OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
auth.set_access_token(credentials.ACCESS_KEY, credentials.ACCESS_SECRET)
api = tweepy.API(auth)

# mention = api.mentions_timeline()
##to find id of recent tweet
# print(mention[0].text)
# print(mention[0].id)

# for tweets in mention:
#     print(tweets.text + '  ' + str(tweets.id))
#     if "hiii " in tweets.text.lower():
#         print("found")

#lastseen_id.txt contains the id of the last responded tweet so that we start responding from the next tweet
# present after last responded tweet so whenever server wakes up a the retrieve function returns the id
# of last responded tweet and before sleep  store function  stores the id of last responded tweet in lastseen file    

def retrieve_lastseen_id(file):
    f_read = open(file,'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_lastseen_id(file,id):
    f_write = open(file,'w')
    f_write.write(str(id)) #store last seen id recieved  in lastseen.txt
    f_write.close()
    return

def reply_to_tweets():
    # mentions = api.mentions_timeline()
    last_seen_id = retrieve_lastseen_id("last_seen_id.txt")
    # the below line provides all the tweets with id greater than lastseen id


    try:
      mentions = api.mentions_timeline( last_seen_id,tweet_mode='extended')  # NOTE: We need to use tweet_mode='extended' below to show all full tweets (with full_text). Without it, long tweets would be cut off.
    except RateLimitError :
      print("Is raised when an API method fails due to hitting Twitter’s rate limit. Makes for easy handling of the rate limit specifically.")
    except TweepError as err:
      print(err)
      mentions = []

    for tweets in reversed(mentions):
        last_seen_id = tweets.id
        print(str(tweets.id) + '_' + tweets.full_text )
        store_lastseen_id("last_seen_id.txt",last_seen_id)
        if "hiii " in tweets.full_text.lower():
            print('found & replying to '+'  '+str(tweets.id) + '_' + tweets.full_text )
            try:
              api.update_status('@' + tweets.user.screen_name +'#Its a reply back to you!', tweets.id)
            except TweepError as err:
              print(err)

while True:
    reply_to_tweets()
    time.sleep(60)