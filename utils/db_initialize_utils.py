import sqlite3

#-------------------------
#FUNCTIONS

def initialize_db():
    
    conn = sqlite3.connect('reddit_data.db') #This will create the db if it doesn't already exist.
    c = conn.cursor()

    # Create tables if they don't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS subreddits (
            name TEXT PRIMARY KEY
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS threads (
            id TEXT PRIMARY KEY,
            subreddit_name TEXT,
            title TEXT,
            author TEXT,
            upvotes INTEGER,
            date_posted TEXT,
            url TEXT,
            content TEXT,
            FOREIGN KEY(subreddit_name) REFERENCES subreddits(name)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id TEXT PRIMARY KEY,
            thread_id TEXT,
            author TEXT,
            upvotes INTEGER,
            date_posted TEXT,
            content TEXT,
            FOREIGN KEY(thread_id) REFERENCES threads(id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS subcomments (
            id TEXT PRIMARY KEY,
            comment_id TEXT,
            author TEXT,
            upvotes INTEGER,
            date_posted TEXT,
            content TEXT,
            FOREIGN KEY(comment_id) REFERENCES comments(id)
        )
    ''')

    conn.commit()
    conn.close()