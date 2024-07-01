import datetime
import pytz
from utils.db_initialize_utils import initialize_db
from utils.db_display_utils import display_data
from utils.reddit_utils import *
from config import *
from prawcore.exceptions import Redirect, NotFound

#-------------------------
#HELPER FUNCTIONS

def get_subreddit(input_value):
    try:
        if input_value.startswith("https://www.reddit.com/r/"):
            subreddit_name = input_value.split('/')[-2]
        else:
            subreddit_name = input_value
        
        #Creates a Subreddit object representing a specific subreddit
        subreddit = reddit.subreddit(subreddit_name)

        # Force a request to check if the subreddit exists
        subreddit.id  # Accessing the subreddit ID to trigger the existence check
        return subreddit
    
    #The Redirect & NotFound exceptions are returned when a subreddit doesn't exist
    except (Redirect, NotFound):
        print(f"Error: The subreddit '{subreddit_name}' does not exist.")
        return None

#-------------------------
#MAIN FUNCTION

def main():

    #Creates reddit_data.db if it doesn't already exist
    initialize_db() 

    #-------------------------
    #COLLECT USER INPUTS & ASSIGN VARIABLES

    subreddit_name_or_url = input("Enter the subreddit name or URL: ").strip()
    date_str = input("Enter the date (YYYY-MM-DD): ").strip()
    start_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    start_date = pytz.utc.localize(start_date)  # Make sure the date is in UTC
    start_timestamp = int(start_date.timestamp())

    #Check if valid subreddit & return subreddit object
    subreddit = get_subreddit(subreddit_name_or_url)

    #End function if subreddit does not exist
    if not subreddit:
        return
    
    #-------------------------
    #ANALYZE EXISTING DATA IN DB FOR SPECIFIC SUBREDDIT
    
    # Initialize empty set variables for existing data
    existing_threads = set()
    existing_comments = set()
    existing_subcomments = set()

    # Retrieve existing IDs from the database
    analyze_existing_data(subreddit, existing_threads, existing_comments, existing_subcomments)
    
    #-------------------------
    #EXTRACT & LOAD DATA FOR SUBREDDIT FROM API
    
    # Initialize empty set variables for API data
    incomming_threads = set()
    incomming_comments = set()
    incomming_subcomments = set()

    # Track IDs coming in from API
    scrape_subreddit(subreddit, start_timestamp, incomming_threads, incomming_comments, incomming_subcomments) 

    #-------------------------
    #DELETE MISSING ENTIRES FROM DB
    thread_diff = existing_threads - incomming_threads
    comments_diff = existing_comments - incomming_comments
    subcomments_diff = existing_subcomments - incomming_subcomments

    delete_missing_entries(thread_diff, 'threads')
    delete_missing_entries(comments_diff, 'comments')
    delete_missing_entries(subcomments_diff, 'subcomments')

    #-------------------------
    #DISPLAY FROM DB
    display_data(subreddit.display_name)

#-------------------------
#RUN MAIN FUNCTION

if __name__ == "__main__":
    main()