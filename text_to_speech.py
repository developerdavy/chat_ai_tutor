from elevenlabs import stream
from elevenlabs.client import ElevenLabs
import os
from langchain.tools import ElevenLabsText2SpeechTool
from dotenv import load_dotenv

load_dotenv()

class TextToSpeech:
    def __init__(self):

        elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        self.client =ElevenLabs(api_key=elevenlabs_api_key)

        self.tts = ElevenLabsText2SpeechTool()

    def convert_to_speech(self, text):

        audio_stream = self.tts.run(text)

        audio_stream.play()

