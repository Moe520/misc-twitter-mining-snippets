
# coding: utf-8
import os
import sys
import time

# This was written for Windows. Mac users adjust accordingly.
# You need to have 2 csv's in your working directory:
## The csv containing your twitter credentials should have them listed in the first 4 rows of the second column
## The csv containing your keywords shuold have them in any column except the first

os.chdir(os.path.dirname(sys.argv[0]))

# In[22]:
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
print("########################################### ")
print("Welcome To Moe's Twitter Listener")
print("########################################## ")
time.sleep(0.5)

# In[23]:
print("")
print("Checking Python Version........")
time.sleep(0.7)
if sys.version_info<(3,0,0):
  print("Python Version 3.0.0 or higher is required")
  time.sleep(4)
  exit(1)
# In[24]:
print(" ")
print(" ")
print("Attempting to Load Dependencies.... ")
print(" ")
time.sleep(0.5)
# In[25]:

import sys


# In[26]:
print(" ")
print("Attempting to load Tweepy ")
time.sleep(0.5)
try:
    import tweepy
    print("Tweepy Loaded Successfully")
except:
    print("Failed To Load Tweepy ")
    print(" Exiting")
    time.sleep(4)
print(" ")


# In[27]:
print(" ")
print("Attempting to Load csv and smtplib libaries ")
time.sleep(0.5)
try:
    import time
    import smtplib
    import os
    import csv
    print("Dependencies Loaded")
except:
     print("Load Error: Please ensure time,os,csv, and smtplib libraries are installed ")
     time.sleep(4)
print(" ")

# In[28]:
time.sleep(1)
print(" ")
print("Current Working Directory is: %s " % os.getcwd() ) 
print(" ")
print(" ")


# In[43]:
print(" ")
print("Retrieving Twitter Credentials from twitter_credentials.csv ...... ")
print(" ")
print(" ")
time.sleep(0.5)
try:
    reader = csv.reader(open("twitter_credentials.csv","r"))
    doc = []
    for row in reader:
        doc.append(row[1:]) # skip first column
    final_list = []
    for row in doc:
        for w in row:
            if (len(w) > 0):
                final_list.append(w.rstrip(' '))
    print("consumer key: %s" % final_list[0])
    print("consumer secret: %s" % final_list[1])
    print("access token: %s" % final_list[2])
    print("access secret: %s" % final_list[3])
except:
    print("Unable To Retrieve Twitter Credentials")
print(" ")
print(" ")
print(" ")
print(" ")

# In[45]:




# In[45]:
print(" ")
print(" ")
print(" ")
print("Testing Twitter Connection....... ")
time.sleep(0.5)
print(" ")

# In[46]:
print("... ")
print("...")
print("... ")
consumer_key = final_list[0]
consumer_secret = final_list[1]
access_token = final_list[2]
access_secret = final_list[3]
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
print(" ")
print(" ")
print(" ")

# In[51]:

try:
    user = tweepy.API(auth).me()
    print('Connection Successful : Twitter Account = ' + user.name)
    print("")
    print("")
    time.sleep(0.5)
except:
    print("Unable to establish connection. Make sure your credentials Are Correct (Try Re-Generating your Tokens")


# In[52]:

allow_email_use = None

while allow_email_use == None:
    print("Allow Email Notifications? (enter yes or no)....")
    print("")
    print("Gmail account required..must have 'allow less secure apps' set to 'on'")
    print("")
    user_answer = input("Do not use this feature if someone else can see you monitor or if on a public network)")

    if user_answer == "yes" :
        time.sleep(1)
        print("Initiating Email Setup")
        allow_email_use = True

    elif user_answer == "no" :
        print("Email Notifications Deactivated")
        allow_email_use = False
    else: 
        print("Please Enter yes or no .... or hit ctrl+c to terminate program ")
        print("")


# In[ ]:




# In[ ]:

#EMail script adapted from http://stackabuse.com/how-to-send-emails-with-gmail-using-python/
if allow_email_use == True:
    import smtplib
    time.sleep(0.5)
    gmail_user = input("Please Enter gmail account")
    time.sleep(0.5)
    gmail_password = input("Please Enter gmail password")

    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        print('Login Attempt Complete. No Errors So Far')
        time.sleep(1)
        print(" ")
        print(" ")
        
    except:  
        print('Failed to Log in to Email Service...Email Notifications Deactivated')
        allow_email_use = False
        pass


# In[53]:
# Put a dummy value if email notifications are disabled
if allow_email_use == False:
    gmail_user = "nothing"
# In[54]:

#EMail script adapted from http://stackabuse.com/how-to-send-emails-with-gmail-using-python/
# function that will send whatever you want to an email address you specify
def send_email(recipient_list=[gmail_user],message="Hello",email_subject='Listener Notification'):
    import smtplib
 
    sent_from = gmail_user  
    to = recipient_list 
    subject = email_subject 
    body = message
    
    email_text = """\  
    From: %s  
    To: %s  
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except:  
        print('Failed to send Email')


# In[ ]:

if allow_email_use == True:
    print("attempting to send test email.........")
    time.sleep(1)
    try:
        send_email(recipient_list=[gmail_user],message="Test Email",email_subject="Test Email")
        print("Test Email Successfully Sent")
    except:
        print("Test Email Failed To Send... Deactivating Email Notifications")
        allow_email_use = False
        pass


# In[ ]:
print(" ")
print(" ")
print(" ")
print("Initializing Twitter Listener.......")
print(" ")
print(" ")


# In[ ]:

# Initializing a listener class that streams from  Twitter
class StdOutListener(tweepy.StreamListener):
    
    #The init function of a class allows us to have variables that  are set to specific values when an instance of the class is intiialized
    # We can then change these attributes from outside the class by calling CLASSNAME.ATTRIBUTENAME = something
    def __init__(self, api=None):
        super(StdOutListener, self).__init__()
        # Initialize the customization attributes that we want to be able to change from the outside 
        self.num_tweets = 0
        self.tweet_limit = 100
        self.file_label = "streamed_tweets"
        self.recipients = 'my_other_email@hotmail.com'
        self.notification_interval = 1000
        self.allow_email = True
        self.allow_progress_email = True
        self.progress_email_interval = 100000
        
    def set_tweet_limit(self,tweet_quantity):
        self.tweet_limit = tweet_quantity
        
    def set_file_label(self,file_label):
        self.file_label = file_label
        
    def set_email_permission(self,allow_email):
        self.allow_email = True
        
    def set_email_recipients(self,email_recipients):
        self.recipients = email_recipients
        
    def set_console_notification_interval(self,console_notification_interval):
        self.notification_interval = console_notification_interval
        
    def set_progress_email_permission(self,progress_email_permission):
        self.allow_progress_email = progress_email_permission
        
    def set_progress_email_interval(self,progress_email_interval):
        self.progress_email_interval = progress_email_interval
    
    def on_data(self, data):
        # Based on the interval chosen by the user, let the user know how many tweets have been collected so far
        if self.num_tweets % self.notification_interval == 0:
            print("(%d) Tweets Collected So far" % self.num_tweets)
            
        # If the user has allowed emails and has chosen to recieve progress emails
        if self.allow_email == True and self.allow_progress_email == True and self.num_tweets % self.progress_email_interval == 0 and self.num_tweets != 0 :
            try:
                send_email(recipient_list=self.recipients,message="(%d) Tweets Collected So Far" %self.num_tweets , 
                           email_subject="Listener Progress Notification")
                print("Progress Email Sent: (%d) tweets collected " % self.num_tweets)
            except:
                print("Failed to send progress email")
                
            
        # Increment the number of tweets collected by 1
        self.num_tweets += 1
        
        # This is the main script that collects the tweets
        # It will terminate when it hits the tweets limit
        if self.num_tweets < self.tweet_limit:
            try:
                with open('%s.json' %self.file_label, 'a') as f:
                    f.write(data)
                    return True
            except KeyboardInterrupt:
                print("Keyboard Interrupt: Ending Stream")
            except BaseException as e:
                print(str(e))
            return True
        else:
            print("Tweet Limit Reached: (%d) .... Closing Stream " % self.num_tweets)
            return False
        
    def on_error(self, status):
        print(status)


# In[ ]:
print(" ")
print(" ")
print(" ")
print("Retrieving Keyword List.........")
time.sleep(1.5)
print(" ")
print(" ")
print(" ")

# In[ ]:


try:
    import csv
    reader = csv.reader(open("Twitter Listener Spreadsheet.csv","r"))
    doc = []
    for row in reader:
        doc.append(row[1:]) # skip first column
    final_list = []
    for row in doc:
        for w in row:
            if (len(w) > 0):
                final_list.append(w.rstrip(' '))
    print(final_list)
    print(" ")
    print(" ")
    print("########################################### ")
except:
    print("Unable To Retrieve Keywords")


# In[ ]:
print(" ")
print(" ")
print(" ")
max_tweets = 0 
while max_tweets == 0:
    max_tweets = int(input("How Many Tweets Would You Like To Collect?"))
    if max_tweets * 0 != 0 :
        print("Please Enter A Valid Number.. or press Ctrl+C to terminate Application")

print(" ")

# In[ ]:

file_label = None

while file_label == None:
    try:
        print("What would you like the output  file to be called?")
        print("")
        print("Do not use quotation marks.  Do Not Use Dots. ")
        print("")
        print("Do Not Use a Number as the first character")
        print("")
        file_label = input("e.g if you want it to be called my_'tweets.json'..... enter 'my_tweets'")
    except:
        print("Input Error: Please enter the name as a string without quotation marks")


# In[ ]:

if allow_email_use == True:
    try:
        print("Who should Recieve The Notification Emails? ")
        print("")
        print("Enter 'me' as the answer if you want them sent to yourself")
        print("")
        recipients = ["%s"%input("Otherwise Enter Recipient's Email")]
    except:
        print("")
        print("Unable to determine Recipients from input.. Will use user's  own email instead")
        recipients = ['%s' %gmail_user] 


# In[ ]:




# In[ ]:

if allow_email_use == True:
    try:
        print("")
        print("")
        time.sleep(1)
        email_notification_interval = int( input("How Often Should an Email Notification be Sent?"))
    except:
        print("Unable to determine input.. Will default to a notification every 500,000 tweets")
        email_notification_interval = 500000
        pass


# In[ ]:

console_interval = 0

while console_interval == 0:
    try:
        print("")
        print("How often should a progress message")
        print("(that says how many tweets have been collected so far)")
        print("appear on the console?")
        console_interval = int( input("(e.g if you want it to show progress every 100th tweet enter '100')"))
    except:
        print("Unable to determine Input: Will Default to update every 100 tweets")


# In[ ]:
print("")
print("")
print("Processing User Inputs........")


# In[ ]:

print(" ")
print(" ")
print("Will Collect %d Tweets....." %max_tweets)
print("")
time.sleep(1)
print("Will Update to Console Every %d Tweets..... " %console_interval)
print("")
time.sleep(1)
print("Output File Will Be Named: %s.json ....." %file_label)

if allow_email_use == True:
    print("")
    time.sleep(1)
    print("Email Notification Enabled.....")
    print("Will Notify Every %d Tweets ......" %email_notification_interval )
print("......Opening Stream.....")
time.sleep(1)

#put a dummy value for email notification rate if email notification is disabled
if allow_email_use != True:
    email_notification_interval = 1000000


# In[ ]:

# Insert dummy values for email recipients if email notification is disabled
if allow_email_use != True:
    recipients = ["nobody"]


# In[ ]:

# Set up function that will initialize this class, and add the constraints we want , 
#as well as filter the feed for the subjects we're interested int
print("")
print("Building Collection Call Function......")
time.sleep(1)
def collect_tweets_from_stream(subjects: object = final_list,
                               max_tweets: object = max_tweets, 
                               file_label: object = file_label,
                               auth: object = auth,
                               email_recipients: object = recipients , 
                               console_notification_interval: object = console_interval , 
                               allow_email: object = allow_email_use,
                               progress_email_permission:object = allow_email_use,
                               progress_email_interval: object = email_notification_interval
                               ) -> object:
    
    my_listener = StdOutListener()
    my_listener.set_tweet_limit(max_tweets)
    my_listener.set_file_label(file_label)
    my_listener.set_email_recipients(email_recipients)
    my_listener.set_console_notification_interval(console_notification_interval)
    my_listener.set_email_permission(allow_email)
    my_listener.set_progress_email_permission(progress_email_permission)
    my_listener.set_progress_email_interval(progress_email_interval)
    
    stream = tweepy.Stream(auth, my_listener)
    
    print("Beginning Stream")
    print("Will collect until %d tweets are reached" %max_tweets )
    print("Output file will be called %s .json " % file_label)
    if allow_email == True :
        print("Email Notifications Are Enabled")
        print("Progress Emails Will Be Sent To : %s" %email_recipients  )

    
    
    try:
        stream.filter(track=subjects)
    except KeyboardInterrupt as e:
        print("Keyboard Interrupt: Stopping Stream")
    except:
        print("Listening function: Termination Caused by Unknown Error")


# In[ ]:
print("")
print("Building Main Function.......")
time.sleep(1)
def main_function():
    
    attempt_count = 0
    while attempt_count < 3:
        print("")
        print("Main Function Attempting To Start")
        time.sleep(1)
        try:
            collect_tweets_from_stream()
            return 
            
        except KeyboardInterrupt as e:
            print("Keyboard interrupt.. Closing Stream")
            return
        except: 
            print("Stream Interrupt Due to Unknown Cause: Will Attempt to Restart After 30 Seconds")
            time.sleep(30)
            attempt_count = attempt_count + 1
    if attempt_count >= 3:
        print("Unable to re-establish connection...Terminating")
        input("Press Enter to Close")
        return


# In[ ]:

main_function()

