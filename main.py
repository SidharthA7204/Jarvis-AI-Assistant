import speech_recognition as sr
import webbrowser
import datetime
import os
import pyttsx3
from openai import OpenAI
from config import apikey

# ---------------------------
# Voice Engine Setup
# ---------------------------
engine = pyttsx3.init()

def say(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# ---------------------------
# OpenAI Setup
# ---------------------------
client = OpenAI(api_key=apikey)

chat_history = []

def chat(query):
    chat_history.append({"role": "user", "content": query})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=chat_history
    )

    reply = response.choices[0].message.content

    chat_history.append({"role": "assistant", "content": reply})

    say(reply)

# ---------------------------
# Speech Recognition
# ---------------------------
def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=6)
        except:
            return "timeout"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-IN")
        print("User:", query)
        return query.lower()

    except:
        return "error"

# ---------------------------
# Main Program
# ---------------------------
if __name__ == "__main__":

    say("Hello, I am Jarvis. How can I help you?")

    while True:

        query = takeCommand()

        if query == "timeout":
            continue

        if query == "error":
            say("Sorry, I didn't understand.")
            continue

        # ---------------------------
        # Website Commands
        # ---------------------------
        if "open youtube" in query:
            webbrowser.open("https://youtube.com")

        elif "open google" in query:
            webbrowser.open("https://google.com")

        elif "open wikipedia" in query:
            webbrowser.open("https://wikipedia.com")

        # ---------------------------
        # Time Command
        # ---------------------------
        elif "time" in query:
            time = datetime.datetime.now().strftime("%H:%M")
            say(f"The time is {time}")

        # ---------------------------
        # Exit Command
        # ---------------------------
        elif "jarvis quit" in query:
            say("Goodbye sir")
            break

        # ---------------------------
        # Chat with AI
        # ---------------------------
        else:
            chat(query)
