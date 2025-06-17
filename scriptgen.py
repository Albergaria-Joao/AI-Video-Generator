from openai import OpenAI
from gtts import gTTS
import os
from icrawler.builtin import GoogleImageCrawler
import wave
from pydub import AudioSegment
from moviepy.editor import *
from PIL import Image
import glob
import time
import whisper
import moviepy.config
import numpy as np
import shutil

moviepy.config.change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("API_KEY"),
)

def generate_script(subject, duration):
    generated = False
    while generated == False:
        messages = [{
            "role": "system",
            "content": (
                "Forget all previous messages"
                "You are a script generator for YouTube Shorts. "
                "Your response must be only the transcription for the voice-over. "
                "Do NOT include any explanations, reasoning, or text inside brackets []. "
                "Your response should be concise and formatted as a script."
                "Always generate a written answer"
            )
        }]

        message = (
            "Forget all previous messages"
            f"Write the script for a {duration}-seconds long YouTube Shorts video about {subject}. "
            "ONLY provide the script, formatted as a voice-over transcription. "
            "DO NOT include any explanations, reasoning, or text inside brackets []. "
            "DO NOT use special characters such as asterisks in your answer"
            "DO NOT use emojis in your answer"
            "Always generate a written answer"
        )

        messages.append(
            {"role": "user", "content": message},
        )

        completions = client.chat.completions.create(
            model="deepseek/deepseek-r1:free", messages=messages
        )
        if completions.choices and completions.choices[0].message.content.strip():
            reply = completions.choices[0].message.content
            if reply != "":
                # Creates the audio using text-to-speech
                print(f"Deepseek: {reply}")
                messages.append({"role": "assistant", "content": reply})
                delete_all('audio/*')
                delete_all('imgs/*')
                language = "en"
                myobj = gTTS(text=reply, lang=language, slow=False)

                myobj.save("audio/audio.mp3")
                generated = True
                return reply
        else:
            return "Curious fact about Batman"

def summarize_script(script):
    generated = False
    while generated == False:
        messages = [{
            "role": "system",
            "content": (
                "Forget all previous messages"
                "You are a summarizer for YouTube Shorts video scripts. "
                "Your response must be only the general subject of the script"
                "Do NOT include any explanations, reasoning, or text inside brackets []. "
                "Your response should be concise and formatted as plain text."
                "Always generate a written answer"
            )
        }]

        message = (
            "Forget all previous messages"
            f"Give me a brief summary of the subject of the following text: {script}. "
            "ONLY provide the subject, formatted as plain text and in few words. "
            "DO NOT include any explanations, reasoning, or text inside brackets []. "
            "DO NOT use special characters such as asterisks in your answer"
            "Always generate a written answer"
        )

        messages.append(
            {"role": "user", "content": message},
        )

        completions = client.chat.completions.create(
            model="deepseek/deepseek-r1:free", messages=messages
        )
        reply = completions.choices[0].message.content

        if reply != "":
            print("REPLY", reply)
            print(f"Deepseek summary: {reply}")
            messages.append({"role": "assistant", "content": reply})
            generated = True
            return reply

def generate_queries(subject, qtt):
    generated = False
    while generated == False:
        messages = [{
            "role": "system",
            "content": (
                "Forget all previous messages"
                "You are a query generator for an image search API"
                "Your response must be only the desired amount of queries"
                "Do NOT include any explanations, reasoning, or text inside brackets []. "
                "DO NOT INCLUDE REASONING"
                "Your response should be concise and formatted as plain text"
                "Always generate a written answer"
            )
        }]

        message = (
            "DO NOT INCLUDE REASONING"
            "Forget all previous messages"
            "Always generate a written answer"
            f"Write {qtt} queries for an image/video search API concerning {subject}. "
            "ONLY provide the queries, separated by &. "
            f"The queries must pertain only to the subject of {subject}"
            "DO NOT include any explanations or reasoning. "
            "Ensure the queries are concise and split using the '&' character."
            "The queries must be separated by &"
        )

        messages.append(
            {"role": "user", "content": message},
        )

        completions = client.chat.completions.create(
            model="deepseek/deepseek-r1:free", messages=messages
        )

        reply = completions.choices[0].message.content
        if reply != "":
            print("REPLY", reply)
            messages.append({"role": "assistant", "content": reply})
            generated = True
            return reply

def delete_all(folder):
    files = glob.glob(folder)
    for file in files:
        os.remove(file)

def get_img_crawler(raw_queries):
    output_dir = 'imgs'
    os.makedirs(output_dir, exist_ok=True)

    # Find current image count
    existing_files = glob.glob(os.path.join(output_dir, '*.*'))
    count = len(existing_files)

    queries = raw_queries.split("&")
    for query in queries:
        crawler = GoogleImageCrawler(storage={'root_dir': output_dir})
        crawler.crawl(keyword=query.strip(), max_num=2)

        # Rename the files
        new_files = sorted(
            glob.glob(os.path.join(output_dir, '0000*.*')),
            key=os.path.getmtime  # Sorting by modification time
        )
        for file_path in new_files:
            ext = os.path.splitext(file_path)[1]
            new_name = f"{count:05d}{ext}"
            new_path = os.path.join(output_dir, new_name)
            shutil.move(file_path, new_path)
            count += 1


def get_audio_duration(file_path):
    audio = AudioSegment.from_file(file_path)
    audio.export("audio/voiceover.wav", format="wav")
    with wave.open('audio/voiceover.wav', 'r') as audio_file:
      frame_rate = audio_file.getframerate()
      n_frames = audio_file.getnframes()
      duration = n_frames / float(frame_rate)
      return duration

# Here, we're resizing the images so they all fit within the selected size
def resize_imgs(target_width, target_height):
    target_size = (target_width, target_height)
    target_w, target_h = target_size
    for img_file in os.listdir("imgs"):
        if img_file.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join("imgs", img_file)
            if img_file.endswith('.png'):
                img = Image.open(img_path).convert("RGBA")
            else:
                img = Image.open(img_path).convert("RGB")
            orig_w, orig_h = img.size
            aspect_ratio = orig_w / orig_h
            
            if orig_w / target_w > orig_h / target_h:
                new_w = target_w
                new_h = int(new_w / aspect_ratio)
            else:
                new_h = target_h
                new_w = int(new_h * aspect_ratio)

            img = img.resize((new_w, new_h), Image.LANCZOS)
            
            # ChatGPT helped me out here, as I was having problems with the RGB channels on PNG images
            if img_file.endswith('.png'):
                new_img = Image.new("RGBA", target_size, (0, 0, 0)) # blank canvas
            else:
                new_img = Image.new("RGB", target_size, (0, 0, 0)) # blank canvas

            paste_x = (target_w - new_w) // 2
            paste_y = (target_h - new_h) // 2
            new_img.paste(img, (paste_x, paste_y))
            new_img.save(img_path)  

# I tried to make better, more dynamic subtitles here but ended up just using this

def generate_subtitles():
    model = whisper.load_model("small")
    transcription = model.transcribe("audio/voiceover.wav")

    subtitles = []
    for segment in transcription["segments"]:
        subtitles.append({
            "text": segment["text"].strip().upper(),
            "start": segment["start"],
            "end": segment["end"]
        })

    return subtitles

def assemble_vid(qtt, subtitles_check, width, height):
    duration = get_audio_duration("audio/audio.mp3")
    fps = qtt/duration
    print(fps)
    resize_imgs(width, height)
    time.sleep(0.5)
    images = sorted(
        [os.path.join("imgs", img) for img in os.listdir("imgs") if img.endswith(('.png', '.jpg', '.jpeg'))]
    )
    if not images:
        print("No images found!")
        return
    else:
        print(images)
    img_clips = []
    clip_duration = duration / len(images)

    for img in images:
        pil_img = Image.open(img).convert("RGB")
        img_array = np.array(pil_img)
        img_clip = ImageClip(img_array, duration=clip_duration)
        img_clips.append(img_clip)

    final_clip = concatenate_videoclips(img_clips, method="compose")

    audio = AudioFileClip("audio/voiceover.wav")
    final_clip = final_clip.set_duration(audio.duration)
    final_video = final_clip.set_audio(audio)
    video_w, video_h = final_video.size

    if (subtitles_check == True):
        subtitles = generate_subtitles()
        print(subtitles)
        subtitle_clips = []
        for sub in subtitles:
            txt_clip = TextClip(sub["text"], fontsize=int(video_h * 0.04), color='yellow', font="Arial-Bold", stroke_color="black", stroke_width=2, method="caption", size=(video_w * 0.9, None))
            txt_clip = txt_clip.set_position(("center", video_h // 2 + 250)).set_start(sub["start"]).set_end(sub["end"])
            subtitle_clips.append(txt_clip)

        final_video = CompositeVideoClip([final_video] + subtitle_clips)

    final_video.write_videofile(f"static/video/video.mp4", codec="libx264", fps=fps)
