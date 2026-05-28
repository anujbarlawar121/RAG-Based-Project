# Converts the videos to mp3
import os
import subprocess

os.makedirs("audios", exist_ok=True)

files = os.listdir("Videos")

for file in files:
    video_path = os.path.join("Videos", file)
    if not os.path.isfile(video_path):
        continue

    tutorial_number = file.split(".")[0]
    file_name = os.path.splitext(file)[0].split(" ", 1)[-1]

    print(tutorial_number, file_name)

    subprocess.run([
        "ffmpeg",
        "-i",
        video_path,
        f"audios/{tutorial_number}_{file_name}.mp3"
    ], check=True)
