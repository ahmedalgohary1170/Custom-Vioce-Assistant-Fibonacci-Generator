import speech_recognition as sr 
import pyttsx3
import nltk 
from nltk.tokenize import word_tokenize
import wikipedia
import pywhatkit
from datetime import datetime

# Ensure required NLTK data is downloaded
nltk.download('punkt')

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech and speak it out loud."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to the microphone and convert speech to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            # Handle case where speech is not recognized
            print("Sorry, I did not understand that.")
            speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            # Handle case where there's a problem with the speech recognition service
            print("Sorry, there was a problem with the speech recognition service.")
            speak("Sorry, there was a problem with the speech recognition service.")
            return None

def process_command(command):
    """Process the given command and return an appropriate response."""
    command = command.lower()  # Convert command to lower case
    tokens = word_tokenize(command)  # Tokenize the command

    if 'hello' in tokens:
        response = "Hello! How can I assist you today?"
    elif 'weather' in tokens:
        response = "Fetching weather information..."
    elif 'time' in tokens:
        now = datetime.now().strftime("%H:%M")
        response = f"The current time is {now}"
    elif 'wikipedia' in tokens:
        try:
            # Search Wikipedia and get a summary
            speak('Searching Wikipedia...')
            command = command.replace('wikipedia', '').strip()
            result = wikipedia.summary(command, sentences=2)
            response = f"According to Wikipedia: {result}"
        except wikipedia.exceptions.DisambiguationError as e:
            response = f"Disambiguation error: {e}"
        except wikipedia.exceptions.PageError:
            response = "Page not found."
        except Exception as e:
            response = f"An error occurred: {e}"
    elif 'play' in tokens:
        song = command.replace('play', '').strip()
        if song:
            # Play the song on YouTube
            response = f'Playing {song}'
            pywhatkit.playonyt(song)
        else:
            response = "No song specified."
    elif 'exit' in tokens:
        response = "Goodbye!"
    else:
        response = "Sorry, I didn't understand that."

    return response

def main():
    """Main function to run the voice assistant."""
    while True:
        command = listen()
        if command:
            response = process_command(command)
            print(response)  # Print the response to the screen
            speak(response)  # Speak the response out loud
            if 'exit' in command.lower():
                break

if __name__ == "__main__":
    main()
