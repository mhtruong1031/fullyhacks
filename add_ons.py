import os
import cv2
import base64

from elevenlabs.client import ElevenLabs
from config import EL_API_KEY

elevenlabs_client = ElevenLabs(api_key=EL_API_KEY)

AUDIO_FOLDER = ""

# ElevenLabs Voice IDs
voice_ids = {
    "brian": "SfKbRWiMPinHRbhypbou",
    "caillou": "FXTfjrw2sZOVFv2ERdxr",
    "chaewon": "hESB0LdnxTU2qjDJP66z",
    "danielle": "0fvxxvs9l2VDSpSQtTqc",
    "drake": "RGlIXmEoMdWfWkpFYbif",
    "felix": "GrZMm10fDuOofyrsqTQd",
    "ferb": "M3qsNO6XANylP7AmUQkI",
    "goofy": "FXTfjrw2sZOVFv2ERdxr",
    "hanni": "o4JtCbuitPnj2SgiuEU9",
    "jungkook": "Vc7U3RawVbaaUT7gQJ2h",
    "karina": "lZguGVnpHrN4p6XnMWsd",
    "kendrick": "5XkAkRgE3SIlLLWzBLLs",
    "lee": "p2vSlfaaqNmog0Wtzktc",
    "minji": "9UMexJQSZUScY3xSnzPP",
    "mickey": "nK82ybbzLlPQRAuZoxIW",
    "patrick": "BjcYkGOFPJUzISUUQQsQ",
    "peter": "w2ndOdlxwHYLpg1zv8Cu",
    "phineas": "lBcCI5qWts12nUcCW0r5",
    "stewie": "ltfUg1WRmlHlH5KXa4gP",
    "spongebob": "C8inc5Ai570PNNKgYMSA",
    "travis": "ULsfwwBnJezY2FmTgPm7",
    "tzuyu": "a07wHmHnd2QUqyQd1W2J",
    "wonyoung": "AEstRh9tiKpbDKjEcqgV",
    "yunjin": "R73PgX77enlYNz3GX65U"
}

def create_audio_folder():
    if not os.path.exists(AUDIO_FOLDER):
        os.makedirs(AUDIO_FOLDER)

def delete_audio_files():
    for audio_file in os.listdir(AUDIO_FOLDER):
        file_path = os.path.join(AUDIO_FOLDER, audio_file)
        os.remove(file_path)
        print(f"Deleted file called {audio_file} at {file_path}")

def save_as_audio_file(generator_object, file_name):
    try:
        file_path = os.path.join(AUDIO_FOLDER, file_name)
        
        with open(file_path, "wb") as file:
            for chunk in generator_object:
                file.write(chunk)
        print(f"Audio saved to {file_path}")
        return file_path 
    except Exception as error:
        print(f"Error saving audio: {error}")

def elevenlabs_generate_voices(script):   
    # To make sure there's an audio folder to clear out/write to
    create_audio_folder()
    # Clear out previous audio files if there were any in the folder
    delete_audio_files()

    dialogues = script["dialogues"]
    voice_file_paths = []
    lineNumber = 1

    for dialogue in dialogues:
        try:
            audio = elevenlabs_client.text_to_speech.convert(
                text=dialogue["line"],
                voice_id=voice_ids[dialogue["voice"]],
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128",
            )
            file_path = save_as_audio_file(audio, f"line_{lineNumber:03d}.mp3")
            if (file_path):
                voice_file_paths.append(file_path)
            else:
                print("Error adding audio's file path to voice_file_paths")

        except Exception as error:
            print(f"Error generating voice for {dialogue['voice']}: {error}")
        lineNumber += 1
    return {"voice_files": voice_file_paths}

# Analyze image for recyclability; returns image path
def take_image(output_path: str = "") -> str:
    path = output_path+'temp.png'

    camera     = cv2.VideoCapture(1)
    for _ in range(5):
        ret, frame = camera.read()

    cv2.imwrite(path, frame)
    camera.release()

    return path

def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")
