# reddit_webscraper

Objective:
This python project scrapes Reddit threads from a specified subreddit, stores the data in a database, and
reads back the stored data to the user.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Notes](#notes)

## Installation

These instructions will guide you through setting up the project on your local machine for development and testing purposes.

### Prerequisites

Make sure you have Python 3.x installed. You can download it from [python.org](https://www.python.org/).

You'll also need `pip` for installing Python packages, which comes bundled with Python.

### Setting Up a Virtual Environment

1. **Clone the Github repository:**

    Replace username with the GitHub username and repository with the name of the repository you want to clone.:

    ```sh
    git clone https://github.com/username/repository.git
    ```

2. **Navigate to the Project Directory:**

    ```sh
    cd reddit_webscraper
    ```

3. **Create a Virtual Environment:**

    ```sh
    python -m venv reddit_webscraper
    ```

4. **Activate the Virtual Environment:**

    - **Windows:**

      ```sh
      reddit_webscraper\Scripts\activate
      ```

    - **macOS/Linux:**

      ```sh
      source reddit_webscraper/bin/activate
      ```

5. **Install Dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

## Reddit API Credentials

1. Navigate to https://www.reddit.com/prefs/apps/
2. Create an app to establish client / secret keys
3. Navigate to config.py in this folder, and fill in client / secret keys within the single quotes.


## Usage

To run the project, make sure your virtual environment is activated and then execute the main script:

```sh
python3 main.py
```

## Notes
- The instructions note the following "A user should be able to enter in a date to scrape back to (e.g. enter date January 1, 2024 the script should pull in all threads from today going back to January 1, 2024). This is expected to
work within the limits of reddit's api."
Per my research, I instead found that using the python library for reddit, praw, is the recommended approach when reading reddit's API via Python. Accordingly, instead of passing in date parameters into the API, the business logic is set up to loop through submissions of a given subreddit. Since submissions are sorted from newest to oldest, we can break when we start seeing submission timestamps prior to the date entered by the user.
- I have noticed instances where the upvote count is different in the UI vs the API. Per my research, it sounds Reddit "fuzzies" votes sometimes to make it harder for users to determine the precise impact of their votes (to defend against spam and gaming the system).
- One way to test out deletes during a subsequent run of a given subresddit is to comment out these lines of code: 
    -- insert_subcomment(subcomment, comment_id)
    -- incomming_subcomments.add(subcomment.id) from reddit_utils.py. Doing so will prevent the script from reading in subcomments, which is a proxy way of assuming that these subcomments have been deleted. In the command line, you should no longer see subcomments.
- There are other strategies to handle deletes (besides the one implemented here). For instance, each time this script runs, we could have assigned it a unique uuid "run_id". This run_id could be included as a key in all the tables. Everytime we see a subsequent run, we could delete anything for a given subreddit that is not affliated to the current run id. The benefit of this approach is that 1) we don't have to analyze the current data before we start calling the API, and 2) we do not have to perform diffs between the existing data in the db and the incoming data from the API to determine what needs to be deleted. The cons are that all tables would have the same key, run_id, which tends to be a slightly less clean data model.