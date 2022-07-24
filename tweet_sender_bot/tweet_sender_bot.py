import tweepy
import time
from random import randrange, choice
import json
import os
import glob
from datetime import datetime

class TweetSenderBot:
    
    DEBUG_MODE = False
    
    def __init__(self,path_to_key_json="twitter_keys.json",path_to_text_files="tweet_text_files"):
        
        print("Fetching API keys...")
        key_dict = json.load(open(path_to_key_json))
        
        print("Instantiating client....")
        
        self.client = tweepy.Client(
            consumer_key=key_dict["api_key"], consumer_secret=key_dict["api_key_secret"],
            access_token=key_dict["access_token"], access_token_secret=key_dict["access_secret"]
        )
        
        
        print("Pulling files with tweets to choose from....")
        tweet_files = glob.glob(path_to_text_files + '/*.txt')
        
        print("Found {} files containing tweets to choose from".format(str(len(tweet_files))))
        
        if self.DEBUG_MODE:
            print(tweet_files)
        
        tweets_to_send_list = []
        
        for tweet_file in tweet_files:
            with open(tweet_file, 'r') as file:
                tweet_body = file.read().replace('\n', '')
                tweets_to_send_list.append(tweet_body)
                
        if self.DEBUG_MODE:
            print(tweets_to_send_list)
            
        self.tweets_to_send_list = tweets_to_send_list
            

    @staticmethod
    def delay(delay_min=1,delay_max=30):
        seconds_to_wait = randrange(delay_min,delay_max)
        print("Will wait {} seconds before sending tweet".format(seconds_to_wait))
        time.sleep(seconds_to_wait)
        
        
    def auto_send_tweet(self,delay_min=1,delay_max=30):
        tweet_body = choice(self.tweets_to_send_list)
        
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        tweet_body = tweet_body + " \n " + dt_string
        
        print("Will send the following tweet after waiting for a random delay")
        print(tweet_body)
        self.delay(delay_min,delay_max)
        
        if self.DEBUG_MODE:
            print("WARNING: Client wrapper is in debug mode. No tweet will be sent")
            print("Would have send tweet:")
            print(tweet_body)
            return
        
        response = self.client.create_tweet(text=tweet_body)
        return response

