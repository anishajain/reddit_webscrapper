import sqlite3
import datetime
import pytz

#-------------------------
#FUNCTIONS

#Insert data into the subreddit table
def insert_subreddit(subreddit):
    conn = sqlite3.connect('reddit_data.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO subreddits (name)
        VALUES (?)
    ''', (subreddit.display_name,))
    conn.commit()
    conn.close()

#Insert data to the threads table
def insert_thread(thread):
    conn = sqlite3.connect('reddit_data.db')
    c = conn.cursor()
    full_url = f"https://www.reddit.com{thread.permalink}"
    c.execute('''
        INSERT OR REPLACE INTO threads (id, title, author, upvotes, date_posted, url, content, subreddit_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (thread.id, #primary key
          thread.title, 
          str(thread.author), 
          thread.score, 
          datetime.datetime.fromtimestamp(thread.created_utc, tz=pytz.utc).isoformat(), 
          full_url, 
          thread.selftext,
          thread.subreddit.display_name)) #foreign key
    conn.commit()
    conn.close()

def insert_comment(comment, thread_id):
    conn = sqlite3.connect('reddit_data.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO comments (id, thread_id, author, upvotes, date_posted, content)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (comment.id, #primary key
          thread_id, #foreign key
          str(comment.author), 
          comment.score, 
          datetime.datetime.fromtimestamp(comment.created_utc, tz=pytz.utc).isoformat(),
          comment.body))
    conn.commit()
    conn.close()

def insert_subcomment(subcomment, comment_id):
    conn = sqlite3.connect('reddit_data.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO subcomments (id, comment_id, author, upvotes, date_posted, content)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (subcomment.id, #primary key
          comment_id, #foreign key
          str(subcomment.author), 
          subcomment.score, 
          datetime.datetime.fromtimestamp(subcomment.created_utc, tz=pytz.utc).isoformat(), 
          subcomment.body))
    conn.commit()
    conn.close()