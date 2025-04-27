import streamlit as st
import pyttsx3
import time
from tutor import AiTutor
import speech_recognition as sr
from elevenlabs import ElevenLabs, stream
import os
from dotenv import load_dotenv

load_dotenv()

tutor = AiTutor()
recognizer = sr.Recognizer()

if "tutor" not in st.session_state:
    st.session_state.tutor = tutor

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🎓 AI Tutor")

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message("You"):
        st.markdown(msg["human"])
    with st.chat_message("Tutor"):
        st.markdown(msg["ai"])

topic = st.sidebar.selectbox(
    "SELECT A TOPIC YOU WANT TO LEARN ABOUT",
    ["Math", "Science", "History", "Geography", "Home Science"]
)

# Function to listen to voice
def listen():
    with sr.Microphone() as source:
        st.info("🎙️ Listening... Speak now.")
        audio = recognizer.listen(source)
    try:
        st.success("✅ Recognizing speech...")
        query = recognizer.recognize_google(audio)
        return query
    except sr.UnknownValueError:
        st.warning("❌ Sorry, I couldn't understand what you said.")
        return None
    except sr.RequestError as e:
        st.error(f"⚠️ Error with speech service: {e}")
        return None

# Text-to-speech
def speak(text):
    engine = pyttsx3.init()
    engine.say(tutor.clean_text_for_speech(text))
    engine.runAndWait()


def eleven_labs_audio(text):
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

    audio_stream = client.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2"
        )
    
    # stream(audio_stream)

    with open("audio.mp3", 'wb') as f:
        for chunk in audio_stream:
            if chunk:
                f.write(chunk)

# Typing input (optional)
user = st.chat_input("Or type your question here...")

# Voice input button
button_area = st.container()

with button_area:
    if st.button("🎙️ Ask with your voice"):
      user = listen()

def markdown_streaming(text, delay=0.05):
    placeholder = st.empty()
    streamed_text = ""
    for word in text.split():
        streamed_text += word + " "
        placeholder.markdown(streamed_text)
        time.sleep(delay)
    return streamed_text

# Handle input
if user:
    with st.chat_message("You"):
        st.markdown(user)

    response = tutor.tutor(user)

    with st.chat_message("Tutor"):
        final_response = markdown_streaming(response)
        # speak(final_response)
        eleven_labs_audio(response)

    st.session_state.messages.append({"human": user, "ai": final_response})


