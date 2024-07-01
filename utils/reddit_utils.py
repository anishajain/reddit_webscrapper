from utils.db_insert_utils import *

#-------------------------
#FUNCTIONS

#For a given subreddit, analyze what data we already have stored in the db. This will help us later with diffing/deleting. 
def analyze_existing_data(subreddit, existing_threads, existing_comments, existing_subcomments):
    conn = sqlite3.connect('reddit_data.db')
    c = conn.cursor()

    print("Analyzing existing data in db for this subreddit...")

    c.execute('SELECT id FROM threads WHERE subreddit_name=?', (subreddit.display_name,))
    threads = c.fetchall()
    existing_threads.update(row[0] for row in threads)

    for thread in threads:
        c.execute('SELECT id FROM comments WHERE thread_id=?',  (thread[0],))
        comments = c.fetchall()
        existing_comments.update(row[0] for row in comments)
        
        for comment in comments:
            c.execute('SELECT id FROM subcomments WHERE comment_id=?', (comment[0],))
            subcomments = c.fetchall()
            existing_subcomments.update(row[0] for row in subcomments)

    conn.close()

    return existing_threads, existing_comments, existing_subcomments

#Call reddit API and scrape data
def scrape_subreddit(subreddit, start_timestamp, incomming_threads, incomming_comments, incomming_subcomments):

    # Insert subreddit into database
    print(f"Starting ingestion for [subreddit] {subreddit.display_name}")
    insert_subreddit(subreddit)

    for submission in subreddit.new(limit=5):
        if submission.created_utc >= start_timestamp:

            print(f"Reading in [subreddit] {subreddit.display_name} // [thread] {submission.title}")
            insert_thread(submission)
            incomming_threads.add(submission.id)    

            # Load comments
            submission.comments.replace_more(limit=None)
            for comment in submission.comments:
                process_comment(comment, submission.id, incomming_comments, incomming_subcomments)
        else:
            # Since submissions are sorted from newest to oldest, we can break early
            break

    return incomming_threads, incomming_comments, incomming_subcomments

#Insert comment into db
def process_comment(comment, thread_id, incomming_comments, incomming_subcomments):
    # Insert comment into database
    insert_comment(comment, thread_id)
    incomming_comments.add(comment.id)

    # Load subcomments
    for subcomment in comment.replies:
        process_subcomment(subcomment, comment.id, incomming_subcomments)

#Insert subcomments into db
def process_subcomment(subcomment, comment_id, incomming_subcomments):
    # Insert subcomment into database
    insert_subcomment(subcomment, comment_id)
    incomming_subcomments.add(subcomment.id)

    # Recursively handle deeper nested subcomments if needed
    for deeper_subcomment in subcomment.replies:
        process_subcomment(deeper_subcomment, subcomment.id, incomming_subcomments)

#Delete data from db wasn't returned from API (ie commenter has deleted their entry)
def delete_missing_entries(missing_ids, table_name):
    conn = sqlite3.connect('reddit_data.db')
    c = conn.cursor()

    for id in missing_ids:
        c.execute(f'DELETE FROM {table_name} WHERE id=?', (id,))

    conn.commit()
    conn.close()
