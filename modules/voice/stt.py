import speech_recognition as sr
import pyttsx3  

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150) 

def speak(text):
    """ Function to convert text to speech """
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()

    speak("I am your script and listening to you. Please speak now.")

    print("I am your script and listening to you...")

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Speak now...")

        try:
            audio = recognizer.record(source, duration=11)
            query = recognizer.recognize_google(audio, language='en-IN')
            print("You said:", query)
            return query
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            speak("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            print("Could not request results; check your internet connection.")
            speak("Could not request results; check your internet connection.")
            return None


