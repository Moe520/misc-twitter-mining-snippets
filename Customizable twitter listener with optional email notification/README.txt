This is an interactive twitter listener with a basic user interface.

It asks the user for thier preferences and streams tweets into a json file based on those preferences.

The twitter credentials (consumer key, secret, etc. are stored in a csv file in the working directory)

The keywords it should search for are stored in another csv also in the working directory.

USER INSTRUCTIONS:

1. open the "Twitter Listener Spreadsheet.csv" and enter the keywords you want to listen for in any column but the first

2. open the "twitter_credentials.csv" and replace the credentials with your own

3. Run the "InteractiveTwitterScript.py" file (in windows: right-click it -> select open with -> python )


Requirements:

Python 3.0 or greater

Tweepy Library (http://www.tweepy.org/)

