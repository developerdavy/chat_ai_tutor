import threading
import time
from tutor import AiTutor
import streamlit as st
import pyttsx3
from text_to_speech import TextToSpeech
import asyncio

tutor = AiTutor()

st.title("AI Tutor")

topic = st.sidebar.selectbox(
    "SELECT A TOPIC YOU WANT TO LEARN ABOUT",
    ["Math", "Science", "History", "Geography", "Home Science"]
)

user = st.chat_input("Enter your question here...")




agent = ""
if user is not None:
    st.write(f"You asked:\n", user)
    agent = tutor.tutor(user)

   

    def stream_agent(agent):
        for word in agent.split(" "):
            yield word + " "
            time.sleep(0.05) # Adjust the delay as needed

    

    def speak(agent):

        engine = pyttsx3.init()
        engine.say(tutor.clean_text_for_speech(agent))

        if engine._inLoop:
            engine.endLoop()

        engine.runAndWait()

    for msg in tutor.show_memory_status():
        print(msg.type, ":", msg.content)
        # engine = None
    
    text = st.write_stream(stream_agent(agent))

    # speak(agent)
   
else:
    st.write("Please enter a question.")
   

