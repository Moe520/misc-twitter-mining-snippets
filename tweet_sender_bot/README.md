# Overview

This is a script that when run, randomly chooses one .txt file from the folder tweet_text_files
and sends the body of that text file as a tweet ( with a timestamp added to it).

# Instructions

1. Edit twitter_keys.json and replace it with your own API credentials. Make sure your developer account has elevated permissions and that the project has read-write permissions BEFORE issuing the API keys.
    
2. In the tweet_text_files folder, put ( each as a separate .txt file ), tweets from which the bot should choose. 

3. Have CRON ( if on linux / mac ) or the Windows task scheduler ( if on Windows ) run auto_send_one_tweet.py periodically. 

