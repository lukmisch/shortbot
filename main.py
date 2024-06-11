import shutil
import sys
import os
import asyncio
from datetime import datetime
from tts import *
from post import *
from video import *
from upload import upload as upload_to_youtube
import discord
from discord.ext import commands

# This will delete all files 
def cleanup(delete_shorts: bool):
    # Delete this directory if it exists, it will cause errors.
    if os.path.isdir('batch'):
        shutil.rmtree('batch')

    # Delete extra files in ingredients folder.
    for filename in os.listdir("ingredients"):
        if filename != "whoosh.mp3":
            file_path = os.path.join("ingredients", filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    if delete_shorts:
        # Delete all existing shorts in folder.
        for filename in os.listdir("shorts"):
            file_path = os.path.join("shorts", filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def create(num_posts):
    # Getting number of posts from arguments.
    print("Generating " + str(num_posts) + " posts...")

    # Retrieving post data from Reddit.

    # Call get_posts with the specified number of top posts
    posts = get_posts(num_posts=num_posts)

    if (posts == False):
        return False
    
    # Creating videos.
    if (create_videos(posts, num_posts) == False):
        return False
    
    # Upload to YouTube.
    upload_to_youtube()
    return True

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

async def loop(client):
    print("Looping...")
    input_arg = sys.argv[1]    # input_arg can also be a link to a specific post
    num_posts = int(input_arg)

    while True:
        current_time = datetime.now()
        # Check if current time is between 6:00 PM and 7:00 PM
        if current_time.hour == 18:
            text_channel = client.get_channel(1248542276800479310)
            if create(num_posts) == True:
                await text_channel.send("Cha-ching!")
            else:
                await text_channel.send("Womp womp...")
        await asyncio.sleep(3600)  # Sleep for 1 hour

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def run():
    TOKEN = 'MTI0ODU0MTA4Mzc5Nzk1MDUxNQ.GzcO61.Yt5IC2MPzxdqaIv56mLOl_KtkVfSb6N6pHTp7A'
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix='!', intents=intents)

    @client.event
    async def on_ready():
        print('Creating content...')
        await loop(client)

    client.run(TOKEN)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

run()
