# speech_input.py

import speech_recognition as sr

recognizer = sr.Recognizer()

def get_voice():
    with sr.Microphone() as source:
        print("\n🎤 Speak a command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text.lower()
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return ""
    except sr.RequestError:
        print("❌ API unavailable")
        return ""