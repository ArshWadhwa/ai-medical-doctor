import os
from gtts import gTTS
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

# gTTS text-to-speech

def text_to_speech_old(input_text, output_filepath):
    language = "en"
    audioobj = gTTS(
        text=input_text,
        lang=language,
    )
    audioobj.save(output_filepath)

input_text = "Hi! this is Arsh"

# ElevenLabs text-to-speech

from dotenv import load_dotenv
# Load environment variables
load_dotenv()
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

def text_to_speech_elevenLabs_old(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio_stream = client.text_to_speech.convert(
        text=input_text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",  # Aria's voice ID
        model_id="eleven_turbo_v2",
        output_format="mp3_22050_32"
    )
    # Save the audio stream to a file
    with open(output_filepath, "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)



    

# text output to voice

import os
from gtts import gTTS
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import subprocess
import platform

# Load environment variables once
load_dotenv()
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

def text_to_speech(input_text, output_filepath):
    language = "en"
    audioobj = gTTS(
        text=input_text,
        lang=language,
    )
    audioobj.save(output_filepath)
    # Autoplay on macOS
    if platform.system() == "Darwin":
        subprocess.run(['afplay', output_filepath])

def text_to_speech_elevenLabs(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio_stream = client.text_to_speech.convert(
        text=input_text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",  # Aria's voice ID
        model_id="eleven_turbo_v2",
        output_format="mp3_22050_32"
    )
    # Save the audio stream to a file
    with open(output_filepath, "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)
    # Autoplay on macOS
    if platform.system() == "Darwin":
        subprocess.run(['afplay', output_filepath])

input_text = "Hi! this is Arsh Wadhwa , new version"


def record_audio(*args, **kwargs):
    # Dummy implementation
    return "Audio recording not implemented."

def transcribe_with_groq(*args, **kwargs):
    # Dummy implementation
    return "Transcription not implemented."