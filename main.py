import pyttsx3
import speech_recognition as sr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import nltk
import random
import joblib
import os  # Import the os module for path operations
import warnings

warnings.simplefilter('ignore')

from Sat import intents
# Load the trained model and vectorizer with adjusted paths
model_path = os.path.join('f:\Satuarday_Advance', 'intent_model.joblib')
vectorizer_path = os.path.join('f:\Satuarday_Advance', 'intent_vectorizer.joblib')

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

def speak(text):
    engine = pyttsx3.init()
    Id = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'
    engine.setProperty('voice', Id)
    print("")
    print(f"==> Saturday : {text}")
    print("")
    engine.say(text=text)
    engine.runAndWait()

def speechrecognition():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source, 0, 8)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language="en")
        print(f"==> user : {query}")
        return query.lower()

    except:
        return ""

def predict_intent(user_input):
    user_input = user_input.lower()
    input_vector = vectorizer.transform([user_input])
    intent = model.predict(input_vector)[0]
    return intent

print("Saturday AI: Hello! How can I assist you?")
while True:
    user_input = speechrecognition()
    if user_input.lower() == 'exit':
        print("Saturday AI: Goodbye!")
        break

    intent = predict_intent(user_input)
    if intent in intents:
        responses = intents[intent]['responses']
        response = random.choice(responses)
        speak(response)

    else:
        speak("Saturday AI: Sorry, I'm not sure how to respond to that.")

