import streamlit as st
import openai
import speech_recognition as sr
from gtts import gTTS
import os
import tempfile
import base64
 
# Initialize OpenAI API

client = openai.OpenAI(api_key="2b4517283c774317a0a7dc00ce887f78")
 
# Streamlit Title
st.title("🗣️ தமிழ் Voice Assistant")
 
# Instructions
st.write("பேசிக் கேளுங்கள், உங்கள் தமிழ் உதவியாளர் பதிலளிக்கிறார்!")
 
# Function to convert speech to text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Speak now...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language="ta-IN")
            return text
        except sr.UnknownValueError:
            return "சொற்கள் புரியவில்லை, தயவுசெய்து மீண்டும் பேசவும்!"
        except sr.RequestError:
            return "குரல் சேவையை அணுக முடியவில்லை!"
 
# Function to generate AI response
def get_ai_response(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "நீங்கள் ஒரு தமிழ் உதவியாளர்."},
                  {"role": "user", "content": user_input}]
    )
    return response['choices'][0]['message']['content']
 
# Function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang="ta")
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    return temp_file.name
 
# Record Speech Button
if st.button("🎙️ Speak"):
    user_text = speech_to_text()
    st.success(f"**You Said:** {user_text}")
 
    if user_text and "சொற்கள் புரியவில்லை" not in user_text:
        # Get AI Response
        ai_response = get_ai_response(user_text)
        st.success(f"**AI Says:** {ai_response}")
 
        # Convert AI response to speech
        audio_file = text_to_speech(ai_response)
        st.audio(audio_file, format="audio/mp3")