import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
import pywhatkit

# -------------------------
# SETTINGS
# -------------------------

NEWS_API_KEY = "YOUR_NEWS_API_KEY"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# -------------------------
# SPEAK FUNCTION
# -------------------------

def speak(text):
    print("Assistant:", text)

    tts = gTTS(text=text, lang='en')
    tts.save("temp.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")


# -------------------------
# AI
# -------------------------

def aiProcess(command):

    client = OpenAI(
        api_key=OPENAI_API_KEY
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a virtual assistant named Jarvis. Give short answers."
            },
            {
                "role": "user",
                "content": command
            }
        ]
    )

    return completion.choices[0].message.content


# -------------------------
# COMMANDS
# -------------------------

def processCommand(command):

    command = command.lower()

    command = command.lower()

    if "google" in command:
        
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")

    elif "linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")

    elif command.startswith("play"):

            song = command.replace("play", "").strip()

            if song:
                speak(f"Playing {song}")
                pywhatkit.playonyt(song)
            else:
                speak("Please tell me the song name.")

                

    elif "news" in command:

        try:
            url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"

            r = requests.get(url)

            if r.status_code == 200:

                data = r.json()

                articles = data.get("articles", [])

                for article in articles[:5]:
                    speak(article["title"])

            else:
                speak("Unable to fetch news.")

        except:
            speak("Error getting news.")

    else:

        try:
            response = aiProcess(command)
            speak(response)

        except Exception as e:
            print(e)
            speak("Sorry, something went wrong.")


# -------------------------
# MAIN
# -------------------------

if __name__ == "__main__":

    speak("Initializing Jarvis")

    while True:

        try:

            with sr.Microphone() as source:

                print("\nListening for wake word...")

                recognizer.adjust_for_ambient_noise(source, duration=1)

                audio = recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=3
                )

            try:

                word = recognizer.recognize_google(audio)

                print("Heard:", word)

                if "jarvis" in word.lower():
                    print("Wake word detected")
                    speak("Yes sir")

                    with sr.Microphone() as source:

                        print("Waiting for command...")

                        recognizer.adjust_for_ambient_noise(source, duration=1)

                        audio = recognizer.listen(
                            source,
                            timeout=5,
                            phrase_time_limit=15
                        )

                    command = recognizer.recognize_google(audio)

                    print("Command:", command)

                    processCommand(command)

            except sr.UnknownValueError:
                print("Could not understand.")

            except sr.RequestError:
                print("Internet error.")

        except Exception as e:
            print("Error:", e)