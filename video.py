import random
import os
import subprocess
import math
import screenshot
import whisper_timestamped
from skimage import filters
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, CompositeVideoClip, ImageClip, TextClip, concatenate_audioclips
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": "D:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"})

session_id = "de396642b46e1edbbb10e8418c31d27a"

# This is a helper for assemble_videos().
# It will assemble a video with the audio.mp3 file in the cd, and
# a random video clip and a random song.
# Returns a tuple of file paths to our randomly chosen video and song.
def random_content() -> (str, str):
    try:
        video_paths = []
        song_paths = []
        # Getting paths to videos and songs to choose from.
        videos_path = "bg_videos"
        for filename in os.listdir(videos_path):
            file_path = os.path.join(videos_path, filename)
            if os.path.isfile(file_path):
                video_paths.append(file_path)
        
        songs_path = "songs"
        for filename in os.listdir(songs_path):
            file_path = os.path.join(songs_path, filename)
            if os.path.isfile(file_path):
                song_paths.append(file_path)

        # Picking random background video and song, and assembling video.
        video = random.choice(video_paths)
        song = random.choice(song_paths)
        print("Using video " + video + " and song " + song)
        return (video, song)
    except:
        print("Error: Failed to generate random content with random_content().")
        return False

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# This is a helper for assemble_videos.
# This will use the "title.txt" and "comment.txt" files that
# are present in our cwd to create .mp3 files for our video.
def create_mp3s():
    # Creating .mp3 file for title.
    command1 = [
        'python3',
        'tts.py',
        '-v', 'en_us_ghostface',
        '-f', 'ingredients/title.txt',
        '-n', 'ingredients/title.mp3',
        '--session', session_id
    ]
    try:
        result = subprocess.run(command1, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error during text-to-speech conversion: {e}")
        return False

    # Creating .mp3 file for comment.
    command2 = [
        'python3',
        'tts.py',
        '-v', 'en_us_ghostface',
        '-f', 'ingredients/body.txt',
        '-n', 'ingredients/body.mp3',
        '--session', session_id
    ]
    try:
        result = subprocess.run(command2, capture_output=True, text=True, check=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during text-to-speech conversion: {e}")
        return False

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    
# This does all the work to glue the video/audio together.
# Takes an integer suffix for the filename, so we don't overwrite videos.
def construct_video(suffix : int):
    try:
        result = random_content()  # Choose random video and song for our clip.
        if (result == False):
            return False
        
        # Getting all of our Video and Audio clips together.
        video = VideoFileClip(result[0])
        song = AudioFileClip(result[1])
        song = song.volumex(0.125)
        whoosh = AudioFileClip("ingredients/whoosh.mp3")
        whoosh = whoosh.volumex(0.5)
        title_audio = AudioFileClip("ingredients/title.mp3")
        comment_audio = AudioFileClip("ingredients/body.mp3")


        # Concatenating our title and comment audio with whoosh in between.
        audio = concatenate_audioclips([title_audio, whoosh])
        title_length = audio.duration   # Saving title length so we can add captions later.
        audio = concatenate_audioclips([audio, comment_audio])
        audio = audio.subclip(0, audio.duration - 0.25)

        # Picking a random start point for song.
        song_start = random.randint(0, math.floor(song.duration) - math.ceil(audio.duration))
        song_end = song_start + audio.duration + 1.25
        song = song.subclip(song_start, song_end)

        # Picking a random start point for video.
        video_start = random.randint(0, math.floor(video.duration) - math.ceil(audio.duration + 1.25))
        video_end = video_start + audio.duration + 1.25
        video = video.subclip(video_start, video_end)

        # Overlaying title card on video and making it slide out.
        slide_out_time = 0.125
        def slide_out(t):
            if t <= title_audio.duration:
                return "center", "center"
            else:
                starting_x = 33
                v = (720 - starting_x) / slide_out_time
                x = starting_x + (t - title_audio.duration) * v
                y = "center"
                return x, y
        
        title = ImageClip("ingredients/title.png").set_start(0).set_duration(title_audio.duration + slide_out_time).set_pos(slide_out)
        video = CompositeVideoClip([video, title])

        # Mixing audio and song.
        audio = CompositeAudioClip([audio, song])
        video.audio = audio

        # Generating subtitles.
        model = whisper_timestamped.load_model("medium")
        result = whisper_timestamped.transcribe(model, "ingredients/body.mp3")

        subs = []
        subs.append(video)
        for segment in result["segments"]:
            for word in segment["words"]:
                text = word["text"].upper()
                start = word["start"] + title_length -.2
                end = word["end"] + title_length -.2
                duration = end - start
                text_clip = TextClip(txt=text, fontsize=80, font="Creepster", stroke_width=4, stroke_color="black", color="white")
                text_clip = text_clip.set_start(start).set_duration(duration).set_pos(("center", "center"))
                subs.append(text_clip)

        video = CompositeVideoClip(subs)

        # Cut video if it's longer than 60 seconds.
        if (video.duration >= 60):
            video = video.subclip(0, 60)

        # Outputting video.
        filename = "shorts/vid" + str(suffix) + ".mp4"
        print("Writing video to " + filename)
        video.write_videofile(filename, temp_audiofile="shorts/temp_audio.mp3")
        return True
    except Exception as e:
        print("Error: Could not construct video.")
        print(e)
        return False

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    
# This will build a script for our video.
# It will also generate a .mp3 file for our audio.
# Then it will call construct_video() to create each video.
def create_videos(posts, num_posts):
    count = 0
    index = 0

    # Continue until we have created the desired amount of posts,
    # or we have tried all 5 posts already.
    while (count < num_posts and index <= 4):
        print("Title: ", posts[index].title)
        print(posts[index].body)
        print(posts[index].url)
    
        # Writing post title and body to file for tts reading.
        try:
            f1 = open("ingredients/title.txt", "w")
            f1.write(posts[index].title)
            f1.close()

            f2 = open("ingredients/body.txt", "w")
            f2.write(posts[index].body)
            f2.close()
        except:
            index += 1
            continue

        # Getting screenshot of the title.
        if (screenshot.getPostScreenshots(posts[index]) == False):
            index += 1
            continue
        
        # Creating .mp3s for our video.
        if (create_mp3s() == False):  # Create .mp3 files for title and comment.
            index += 1
            continue
        
        # Building our videos.
        if (construct_video(count + 1) == False):  # Actually creating the videos.
            index += 1
            continue
        
        index += 1
        count += 1

