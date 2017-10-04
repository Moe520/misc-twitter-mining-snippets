import os
import sys
import time

# Errors dictionary
ht_err = {0: 'Python version 3.0.0 or higher is required...',
		  1: 'Failed to load Tweepy...',
		  2: 'smtplib library not installed...',
		  3: 'csv library not installed...',
		  4: 'Unable to retrieve Twitter credentials... ',
		  5: 'Unable to establish connection. Make sure your credentials\n \
			  are correct (Try re-generating your tokens).',
		  6: 'Unable to retrieve keywords list...',
		  7: 'Keyboard interrupt, stopping stream...',
		  8: 'Unable to re-establish connection...'}

def c_exit(err_id):
	print ("ERROR: " + ht_err[err_id])
	print ("Exiting now...")
	time.sleep(1)
	exit(1)

# Check python version
def check_version():
	print("\n\nChecking Python Version...")
	time.sleep(0.7)
	if sys.version_info<(3,0,0):
		c_exit(0)
	return

# Load dependencies as global, define listener class (depends on tweepy)
def load_libs():
	print("\nAttempting to load dependencies.... ")
	# Load Tweepy
	print("\n\tAttempting to load Tweepy: ")
	time.sleep(0.5)
	try:
		global tweepy
		tweepy = __import__('tweepy', globals())
		print("\tTweepy loaded successfully...")
	except:
		c_exit(1)
	# Load smtplib
	print("\n\tAttempting to load smtplib: ")
	time.sleep(0.5)
	try:
		global smtplib
		smtplib = __import__('smtplib', globals())
		print ("\tsmtplib loaded successfully...")
	except:
		c_exit(2)
	# Load csv
	print("\n\tAttempting to load csv library: ")
	time.sleep(0.5)
	try:
		global csv
		csv = __import__('csv', globals())
		print ("\tcsv loaded successfully...")
	except:
		c_exit(3)
	
	# Define listener class (must be here since it inherits from tweepy)
	global StdOutListener
	class StdOutListener(tweepy.StreamListener):
		#The init function of a class allows us to have variables that  are set to specific values when an instance of the class is intiialized
		# We can then change these attributes from outside the class by calling CLASSNAME.ATTRIBUTENAME = something
		def __init__(self, api=None):
			super(StdOutListener, self).__init__()
			self.num_tweets = 0
			self.tweet_limit = 0
			self.file_label = "streamed_tweets"
			self.recipients = "email"
			self.notification_interval = None
			self.allow_email = None
			self.allow_progress_email = None
			self.progress_email_interval = None
		
		def set_tweet_limit(self,tweet_quantity):
			self.tweet_limit = tweet_quantity
		
		def set_file_label(self,file_label):
			self.file_label = file_label
		
		def set_email_recipients(self,email_recipients):
			self.recipients = email_recipients
		
		def set_email_permission(self,allow_email):
			self.allow_email = allow_email
		
		def set_console_notification_interval(self,console_notification_interval):
			self.notification_interval = console_notification_interval
		
		def set_progress_email_permission(self,progress_email_permission):
			self.allow_progress_email = progress_email_permission
		
		def set_progress_email_interval(self,progress_email_interval):
			self.progress_email_interval = progress_email_interval
		
		def on_data(self, data):
			# Based on the interval chosen by the user, let the user know 
			# how many tweets have been collected so far
			if (self.num_tweets % self.notification_interval == 0):
				print("\t" + str(self.num_tweets) + " tweets collected...")
			
			# If the user has allowed emails and has chosen to recieve progress emails
			if (self.allow_email and self.allow_progress_email 
				and (self.num_tweets % self.progress_email_interval == 0) and (self.num_tweets != 0)):
				try:
					send_email(recipient_list=self.recipients,
						message=str(self.num_tweets) + " tweets collected..." , 
						email_subject="Listener Progress Notification")
					print("Progress Email Sent: (%d) tweets collected " % self.num_tweets)
				except:
					print("Failed to send progress email")
			
			# Increment the number of tweets collected by 1
			self.num_tweets += 1
			
			# Open file where to save tweets
			#f = open('%s.json' %self.file_label, 'a')
			
			# This is the main script that collects the tweets
			# It will terminate when it hits the tweets limit
			if (self.num_tweets < self.tweet_limit):
				try:
					with open('%s' %self.file_label, 'a') as f:
						f.write(data)
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
		
		def on_timeout(self, status):
			print('Stream disconnected; continuing...')
		
	return

# Return tweeter credentials in a dictionary
def get_credentials():
	print("\nRetrieving Twitter credentials... ")
	credentials = {}
	time.sleep(0.5)
	print("\n\tAttempting to retireve Twitter credentials from environment variables...")
	time.sleep(0.1)
	try:
		credentials["consumer_key"] = os.environ['TWEET_CONSUMER_KEY'] 
		credentials["consumer_secret"] = os.environ['TWEET_CONSUMER_SECRET'] 
		credentials["access_token"] = os.environ['TWEET_ACCESS_TOKEN'] 
		credentials["access_secret"] = os.environ['TWEET_ACCESS_SECRET'] 
	except:
		print ("\tNo environment variables found... ")
		time.sleep(0.5)
		print("\n\tAttempting to retireve Twitter credentials from twitter_credentials.csv... ")
		time.sleep(0.1)
		try:
			f = open("twitter_credentials.csv","r")
			for idx,line in enumerate(f):
				# Skip first row
				if (idx == 0):
					continue
				# Read in row, strip \n, split and save key
				line = line.rstrip('\n').split(',')
				credentials[line[0]] = line[1]
			f.close()
		except:
			c_exit(4)
	return credentials

# Check credentials via connection
def check_connection(credentials):
	print("\nTesting Twitter connection... ")
	time.sleep(0.5)
	auth = tweepy.OAuthHandler(credentials["consumer_key"], credentials["consumer_secret"])
	auth.set_access_token(credentials["access_token"], credentials["access_secret"])
	try:
		user = tweepy.API(auth).me()
		print('\n\tConnection successful...\n\tTwitter Account = ' + user.name)
		time.sleep(0.5)
	except:
		c_exit(5)
	return auth

# Check email notifications option
def check_email():
	allow_email_use = None
	while (allow_email_use is None):
		print("\nEmail notifications activation (do not use this feature if")
		print("someone else can see you monitor or if on a public network)...")
		print("For email notifications a GMAIL account is required")
		print("(you must have 'allow less secure apps' set to 'on')...")
		user_answer = input("\n\tAllow email notifications? (yes/no) ")
		if user_answer == "yes":
			time.sleep(0.5)
			print("\n\tInitiating email setup...")
			allow_email_use = True
		elif user_answer == "no" :
			print("\n\tEmail notifications disabled...")
			allow_email_use = False
		else: 
			print("\n\tPlease enter yes or no.... or use ctrl+c to terminate the program...")
	# EMail script adapted from 
	# http://stackabuse.com/how-to-send-emails-with-gmail-using-python/
	time.sleep(0.5)
	if (allow_email_use):
		gmail_user = input("\n\tPlease enter gmail account: ")
		time.sleep(0.1)
		try:
			import getpass
			gmail_password = getpass.getpass("\tPlease enter gmail password: ")
		except:
			gmail_password = input("\tPlease enter gmail password: ")
		# Try to connect to server
		try:  
			server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			server.ehlo()
			server.login(gmail_user, gmail_password)
			print('\n\tGmail server login attempt completed successfully...')
			print("\t Attempting to send test email...")
			allow_email_use = send_email(gmail_user)
		except:
			print ("\n\tFailed to log in to email service... Email notifications disabled...")
			allow_email_use = False
			gmail_user = ""
			gmail_password = ""
	else:
		gmail_user = ""
		gmail_password = ""
		
	time.sleep(0.5)
	
	if (allow_email_use):
		try:
			print("\n\tWho should receive the notification emails? ")
			print("\tEnter 'me' as the answer if you want them sent to yourself,")
			recipients = input("or enter recipient's email: ")
		except:
			print("\n\tUnable to determine recipients from input. Will use user's own email instead...")
			recipients = gmail_user
		try:
			email_notification_interval = int( input("\n\tInsert number of tweets interval at which email notification will be sent: "))
		except:
			try:
				email_notification_interval = int( input("\tInsert a valid number: "))
			except:
				print ("\tUnable to determine input... Will default to a notification every 500 000 tweets...")
				email_notification_interval = 500000
	else:
		email_notification_interval = None
		recipients = ""
	
	# Save in dictionary
	email_opt = {}
	email_opt['user'] = gmail_user
	email_opt['pass'] = gmail_password
	email_opt['recip'] = recipients
	email_opt['allow'] = allow_email_use
	email_opt['interval'] = email_notification_interval
	
	return email_opt

# EMail script adapted from 
# http://stackabuse.com/how-to-send-emails-with-gmail-using-python/
# Function that will send whatever you want to an email address you specify
def send_email(gmail_user,message="Hello we are trying to connect!",
	email_subject='Listener Notification'):
	
	sent_from = gmail_user  
	to = gmail_user 
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
		print('Test email sent... ')
		return True
	except:  
		print('Failed to send test email... ')
		return False

# Read keywords from csv file
def retrieve_keys():
	print("\nRetrieving Keyword list...")
	try:
		reader = csv.reader(open("Twitter Listener Spreadsheet - Sheet1.csv","r"))
		doc = []
		for row in reader:
			doc.append(row[1:]) # skip first column
		final_list = []
		for row in doc:
			for w in row:
				if (len(w) > 0):
					final_list.append(w.rstrip(' '))
		print(final_list)
	except:
		c_exit(6)
	
	return final_list 

# Ask for number of tweets to be collected
def set_number_tweets():
	condition = False
	max_tweets = None
	while (not condition):
		max_tweets = (input("\nHow many tweets do you want to collect? "))
		try:
			max_tweets = int(max_tweets)
			condition = True
		except:
			print('\tPlease enter a valid number... or press ctrl+c to terminate application...')
	
	return max_tweets

# Ask for output file name where to write collected tweets
def set_file_name():
	
	file_name = ''
	while (len(file_name) <= 0):
		file_name = input('\nEnter name of file where tweets will be stored: ')
		file_name = file_name.replace('.','')
		file_name = file_name.replace('"','')
		file_name = file_name.replace('\\','')
		file_name = file_name.replace(' ','_')
		file_name += '.json'
		print('The tweets will be saved in ' + str(file_name))
	
	return file_name

# Ask for console updates
def set_console_message():
	console_interval = None
	while (console_interval is None):
		try:
			console_interval = int( input("\nAfter how many tweets should the console notify you? "))
		except:
			print("\tUnable to determine input... Will default to update every 100 tweets...")
			console_interval = 100
	
	return console_interval

# Set listener parameters
def initialize_listener(max_tweets, file_label, recipients, console_interval,
						allow_email_use,email_notification_interval):
	
	print("\nInitializing listener... ")
	time.sleep(0.5)
	
	# Initialize listener
	my_listener = StdOutListener()
	my_listener.set_tweet_limit(max_tweets)
	my_listener.set_file_label(file_label)
	my_listener.set_email_recipients(recipients)
	my_listener.set_console_notification_interval(console_interval)
	my_listener.set_email_permission(allow_email_use)
	my_listener.set_progress_email_permission(allow_email_use)
	my_listener.set_progress_email_interval(email_notification_interval)
	
	return my_listener

# Stream from twitter and collect data
def collect_stream(my_listener,auth,keywords):
	
	count = 1
	# Maximum connections: 3 in 15 minutes
	while (count < 4):
		print ("\nConnecting listener to stream...")
		time.sleep(0.5)
		stream = tweepy.Stream(auth, my_listener)
		try:
			print("\n\tStreaming now...")
			stream.filter(track=keywords)
			return
		# If keybord exit interrupt
		except KeyboardInterrupt as e:
			c_exit(7)
		except:
			print("\n\tListening function: Termination Caused by Unknown Error...")
			print("\tWill attempt restart after 30 seconds...")
			for s in range(30):
				print("\t"+"\r"+str(s), end='')
				time.sleep(1)
		
		stream.disconnect()
		
		count += 1
	
	if count == 2:
		c_exit()
	
	return

# Main wrapper function
def main():
	#os.chdir(os.path.dirname(sys.argv[0]))
	print("\n\n\n\n########################################### ")
	print("Welcome To Moe's Twitter Listener")
	print("########################################## ")
	time.sleep(0.5)
	# Check python version
	check_version()
	# Load Libraries
	load_libs()
	# Get twitter keys
	credentials = get_credentials()
	# Check connection
	auth = check_connection(credentials)
	# Check email notifications option
	email_options = check_email()
	# Retrieve keys from csv file
	keywords = retrieve_keys()
	# Set maximum number of tweets to be collected
	max_tweets = set_number_tweets()
	# Ask for output file name
	file_label = set_file_name()
	# Ask for console updates
	console_interval = set_console_message()
	# Initialize listener
	my_listener = initialize_listener(max_tweets, file_label, email_options['recip'], 
		console_interval, email_options['allow'],email_options['interval'])
	# Stream
	collect_stream(my_listener,auth,keywords)
	
	return

# Start script
main()
