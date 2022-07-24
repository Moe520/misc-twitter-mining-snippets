from tweet_sender_bot import TweetSenderBot
from datetime import datetime

MIN_DELAY_SECONDS = 2
MAX_DELAY_SECONDS = 45
WRITE_REPORT_TO_FILE_ON_SUCCESS = True

print("Instantiating wrapper class...")
bot = TweetSenderBot()
response = bot.auto_send_tweet(MIN_DELAY_SECONDS,MAX_DELAY_SECONDS)
print("Send action complete..")

if WRITE_REPORT_TO_FILE_ON_SUCCESS:
    print("Writing success report to completion_reports.txt .....")
    
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    sent_text = str(response.data['text']).strip().replace('\n', ' ').replace('\r', '')
    report_msg = "\n Sent tweet containing: ( {} ) at date and time: {}".format(str(sent_text),str(dt_string))

    with open("completion_reports.txt", "a") as file_object:
        file_object.write(report_msg)