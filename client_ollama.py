import requests
import pyttsx3
import serial
import speech_recognition as sr
import re

# Configura la porta seriale COM5
serial_port = serial.Serial('/dev/ttyUSB0', 9600)

# Configura il motore di sintesi vocale
text_to_speech_engine = pyttsx3.init()
text_to_speech_engine.setProperty('rate', 130)  # Imposta la velocità
text_to_speech_engine.setProperty('voice','italian')

# Configura il riconoscimento vocale
recognizer = sr.Recognizer()

def speak(text):
    """Converti il testo in parlato dopo aver rimosso caratteri speciali."""
    cleaned_text = re.sub(r"[^\w\s.,!?]", "", text)
    text_to_speech_engine.say(cleaned_text)
    text_to_speech_engine.runAndWait()

def send_to_serial(text):
    """Invia il testo alla porta seriale."""
    serial_port.write((text + '\n').encode())

def listen():
    """Ascolta l'input vocale finché non rileva una frase."""
    with sr.Microphone() as source:
        print("Ascoltando... (parla per porre una domanda)")
        recognizer.adjust_for_ambient_noise(source)  # Riduce il rumore di fondo
        audio = recognizer.listen(source)  # Ascolta l'audio

    try:
        text = recognizer.recognize_google(audio, language='it-IT')
        print(f"Tu: {text}")
        return text
    except sr.UnknownValueError:
        print("Non ho capito cosa hai detto, continua a parlare...")
        return ""
    except sr.RequestError:
        print("Errore di richiesta con il servizio di riconoscimento vocale")
        return ""

# Indirizzo del server Flask
SERVER_URL = "http://213.233.44.94:5000/generate"

a = ""
while a.lower() != "brake":
    a = listen()  # Ascolta l'input vocale
    if a.lower() != "brake" and a != "":
        # Invia il prompt al server
        response = requests.post(SERVER_URL, json={"prompt": a})

        if response.status_code == 200:
            data = response.json()
            if "chunks" in data:
                for chunk in data["chunks"]:
                    print(f"Risposta: {chunk}")
                    send_to_serial(chunk)
                    speak(chunk)  # Pronuncia la risposta
        else:
            print(f"Errore nel server: {response.text}")

# Chiudi la porta seriale prima di uscire
serial_port.close()
