import speech_recognition as sr
import pyttsx3
import datetime
import requests
from bs4 import BeautifulSoup

# Initialize the speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            print("Sorry, there seems to be a problem with the request.")
            return ""

def get_time():
    now = datetime.datetime.now()
    return now.strftime("%H:%M")

def get_date():
    today = datetime.datetime.now()
    return today.strftime("%Y-%m-%d")

def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    result_div = soup.find_all('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'})
    
    if result_div:
        return result_div[0].text
    else:
        return "No results found."

def handle_command(command):
    if "hello" in command:
        speak("Hello! How can I assist you today?")
    elif "time" in command:
        current_time = get_time()
        speak(f"The current time is {current_time}")
    elif "date" in command:
        current_date = get_date()
        speak(f"Today's date is {current_date}")
    elif "search" in command:
        query = command.replace("search", "").strip()
        if query:
            result = search_web(query)
            speak(result)
        else:
            speak("Please provide a search query.")
    else:
        speak("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    while True:
        command = listen()
        if command:
            handle_command(command)
