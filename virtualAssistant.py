import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import pywhatkit
import subprocess

# Initialize the speech engine
engine = pyttsx3.init()

# Set speech rate and volume
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

# Function to make the assistant speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to take voice commands
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print(f"Command: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Please repeat.")
            return None  # return None if command is not recognized
        except sr.RequestError:
            speak("Sorry, I'm having trouble connecting to the internet.")
            return None

# Function to open and close files
def handle_files(command):
    if 'open file' in command:
        speak("Please specify the file name.")
        file_name = take_command()
        if file_name:
            try:
                os.startfile(file_name)
                speak(f"Opening {file_name}")
            except FileNotFoundError:
                speak(f"Sorry, I couldn't find {file_name}.")
        else:
            speak("No file name provided.")
    elif 'close file' in command:
        speak("Please specify the file to close.")
        file_name = take_command()
        if file_name:
            try:
                os.system(f"taskkill /f /im {file_name}")
                speak(f"Closing {file_name}")
            except Exception:
                speak(f"Sorry, I couldn't close {file_name}.")
        else:
            speak("No file name provided.")

# Function to search on Google and YouTube
def search_web(command):
    if 'google' in command:
        speak("What should I search for?")
        search_query = take_command()
        if search_query:
            pywhatkit.search(search_query)
            speak(f"Searching for {search_query} on Google.")
        else:
            speak("No search query provided.")
    elif 'youtube' in command:
        speak("What video should I search for?")
        video_query = take_command()
        if video_query:
            pywhatkit.playonyt(video_query)
            speak(f"Playing {video_query} on YouTube.")
        else:
            speak("No video query provided.")

# Function to play music (assuming mp3 files)
def play_music():
    speak("Playing your music")
    music_dir = 'C:\\path_to_your_music_folder'  # Specify your music folder path
    songs = os.listdir(music_dir)
    if songs:
        os.startfile(os.path.join(music_dir, songs[0]))
    else:
        speak("I couldn't find any music files in the directory.")

# Main assistant function
def voice_assistant():
    while True:
        speak("How can I assist you?")
        command = take_command()

        if command:
            if 'open file' in command or 'close file' in command:
                handle_files(command)
            elif 'search on google' in command or 'youtube' in command:
                search_web(command)
            elif 'play music' in command:
                play_music()
            elif 'exit' in command or 'quit' in command:
                speak("Goodbye!")
                break
            else:
                speak("I didn't understand that. Please try again.")
        else:
            speak("No command detected, please repeat.")

if __name__ == "__main__":
    voice_assistant()
