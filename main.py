import shutil
import sys
import upload
from tts import *
from post import *
from video import *

# This will delete all files 
def cleanup(delete_shorts : bool):
    # Delete this directory if it exists, it will cause errors.
    if (os.path.isdir('batch')):
        shutil.rmtree('batch')

    # Delete extra files in ingredients folder.
    for filename in os.listdir("ingredients"):
        if filename != "whoosh.mp3":
            file_path = os.path.join("ingredients", filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    if (delete_shorts):
        # Delete all existing shorts in folder.
        for filename in os.listdir("shorts"):
            file_path = os.path.join("shorts", filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def main():
    # First let's clean the folders in case of previously failed execution.
    cleanup(True)

    # Getting number of posts from arguments.
    num_posts = int(sys.argv[1])
    print("Generating " + str(num_posts) + " posts...")

    # Retrieving post data from Reddit.
    posts = get_posts(num_posts)
    if (posts == False):
        return False
    
    # Creating videos.
    if (create_videos(posts, num_posts) == False):
        return False
    
    # Upload to YouTube.
    upload.upload()

    # Cleanup again.
    cleanup(False)

    print("Cha-ching!")

if __name__ == "__main__":
    main()
