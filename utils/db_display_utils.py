import sqlite3
import textwrap

#-------------------------
#FUNCTIONS

def display_data(subreddit_name):
    conn = sqlite3.connect('reddit_data.db')
    c = conn.cursor()
    
    # Print thread
    c.execute('SELECT * FROM threads WHERE subreddit_name=?', (subreddit_name,)) #Pass in subreddit name of interest.
    threads = c.fetchall()
    for thread in threads: #Loop through all threads
        print_thread(thread)

        # Fetch and print comments for this thread
        c.execute('SELECT * FROM comments WHERE thread_id=?', (thread[0],))
        comments = c.fetchall()
        for comment in comments:
            print_comment(comment)

    conn.close()

def print_thread(thread):
    print('-' * 20)
    print(f"Thread Title: {thread[2]}")
    print(f"Original Post: {thread[7]}")
    print(f"Username: {thread[3]}")
    print(f"Upvotes: {thread[4]}")
    print(f"Date: {thread[5]}")
    print(f"URL: {thread[6]}")
    print('-' * 20)

def print_comment(comment):
    print(f"  Comment by: {comment[2]}")
    print(f"  Upvotes: {comment[3]}")
    print(f"  Date: {comment[4]}")
    wrapped_comment = textwrap.indent(textwrap.fill("Comment Text: " + comment[5], width=100), '  ')
    print(wrapped_comment)
    print('-' * 20)

    # Fetch and print subcomments recursively
    fetch_and_print_subcomments(comment[0], indent_level=4)

def print_subcomment(subcomment, indent_level):
    indent = ' ' * indent_level
    print(f"{indent}Subcomment by: {subcomment[2]}")
    print(f"{indent}Upvotes: {subcomment[3]}")
    print(f"{indent}Date: {subcomment[4]}")
    wrapped_subcomment = textwrap.indent(textwrap.fill("Subcomment Text: " + subcomment[5], width=100), indent)
    print(wrapped_subcomment)
    print('-' * 20)

    # Fetch and print deeper subcomments recursively
    fetch_and_print_subcomments(subcomment[0], indent_level + 4)

#Both comments and subcomments can have subcomments. This loops through subcomments and prints them.
def fetch_and_print_subcomments(comment_id, indent_level):
    conn = sqlite3.connect('reddit_data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM subcomments WHERE comment_id=?', (comment_id,))
    subcomments = c.fetchall()
    conn.close()

    for subcomment in subcomments:
        print_subcomment(subcomment, indent_level)