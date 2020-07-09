#!/usr/bin/python3

import praw
import subprocess
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit("buildapcsales")

# Have we run this code before? If not, create an empty list
if not os.path.isfile("Log.txt"):
	log = []
else:
	# If we have run the code before, load the list of posts we have replied to
	with open("Log.txt", "r") as f:
		log = f.read()
		log = log.split("\n")
		log = list(filter(None, log))

for submission in subreddit.new(limit=10):
	print("Title: ", submission.title)
	post_title = submission.title
	post_id = submission.id
	item_url = submission.url
	post_link = "old.reddit.com" + submission.permalink

	product_list = open('Product List.txt').read().splitlines()
	#previous_deals = open('Log.txt').read().splitlines()

	for x in product_list:
		pc_part = x

		if pc_part in post_title:
			 # If we haven't replied to this post before
			if submission.id not in log:
				# Store the current id into our list
				log.append(submission.id)
				# Write our updated list back to the file
				with open("Log.txt", "w") as f:
					for post_id in log:
						f.write(post_id + "\n")

				port = 465  # For SSL
				smtp_server = "smtp.gmail.com"

				sender_email = "buildapcsalespricetracker@gmail.com"
				password = "PythonBot#%"

				message = MIMEMultipart("alternative")
				message["Subject"] = "Sale Alert"
				message["From"] = sender_email

				html = """
				<html>
				  <body>
				    <p>According to <a href="{link}">Reddit: {title}</a>,<br><br>
				    	{item} is on sale <a href="{url}">here</a><br><br>
				    </p>
				  </body>
				</html>
				""".format(link=post_link,item=pc_part, url=item_url,title=post_title)

				message_body = MIMEText(html, "html")
				message.attach(message_body)

				contact_list = open('Contact List.txt').read().splitlines()

				context = ssl.create_default_context()
				with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
					server.login(sender_email, password)

					for y in contact_list:
						receiver_email = y
						message["To"] = receiver_email
						server.sendmail(sender_email, receiver_email, message.as_string())
