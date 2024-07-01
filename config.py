import praw

#-------------------------
#VARIABLES

client_id = ''
client_secret = ''
user_agent = 'web-scraper'

#-------------------------
#CREATE A REDDIT INSTANCE

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)