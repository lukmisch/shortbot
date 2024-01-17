import praw
import re
from praw.models import MoreComments

# Here is a class that will represent a post.
# It carries all the necessary post information we will need.
class Post:
    def __init__(self, id, title, url, body):
        self.id = id
        self.title = title
        self.body = body
        self.url = url

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# This cleans up text for text to speech.
# It will:
# 1. Remove links.
# 2. Remove newlines.
# 3. Remove asterisks (cause apparently people like to use those).
# 4. Replaces all non-unicode characters.
def clean_text(text : str) -> str:
    try:
        hyperlink_pattern = r'https?://\S+|www\.\S+'
        
        # Use re.sub to replace hyperlinks with an empty string.
        text = re.sub(hyperlink_pattern, '', text)

        # Replacing newlines and collapsing spaces.
        text = text.replace('\n', ' ')
        text = re.sub(' +', ' ', text, count=0)
        text = text.replace('*', '')
        return text
    except:
        print("Error: Failed to clean text in clean_text().")

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Gets a post that we want to use.
# Returns a list of post objects
def get_posts(num_posts : int) -> [Post]:
    try:
        # Here is the list where we will keep track of our posts.
        posts = []

        # Creating reddit instance with praw.
        reddit = praw.Reddit(
            client_id = "KkTPY_6xiK77pDW8qi2tIg",
            client_secret = "aPLTdCla6wTE0o9B3oXUXYczi60TBQ",
            user_agent = "my-app by u/LukMisch"
        )

        # Here we will specify the subreddit.
        subreddit = reddit.subreddit("TwoSentenceHorror")
        top_posts = subreddit.top(time_filter="day", limit=5)

        # Getting top posts for the day.
        for post in top_posts:
            new_post = Post(post.id, clean_text(post.title), post.url, post.selftext)
            posts.append(new_post)
        
        return posts
    except:
        print("Error: Failed to get posts with get_posts().")
        return False
