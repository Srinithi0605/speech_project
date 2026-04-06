# actions.py

import webbrowser
import os
import time
import json
import pyautogui
import pyttsx3
from difflib import get_close_matches
from datetime import datetime

engine = pyttsx3.init()

FILE_INDEX = []
INDEX_FILE = "file_index.json"

# 🔥 UNIVERSAL APP MAP
SPECIAL_APPS = {
    "spotify": "spotify:",
    "settings": "ms-settings:",
    "photos": "ms-photos:",
    "calculator": "calc",
    "whatsapp": "whatsapp:",
    "camera": "microsoft.windows.camera:",
    "explorer": "explorer",
    "file explorer": "explorer",
}


def speak(text):
    print("🤖", text)
    engine.say(text)
    engine.runAndWait()


# 🔥 FILE INDEX
def build_index():
    global FILE_INDEX

    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            FILE_INDEX = json.load(f)
        return

    speak("Indexing files, please wait")

    for root, dirs, files in os.walk("C:\\Users"):
        for name in dirs + files:
            FILE_INDEX.append((name.lower(), os.path.join(root, name)))

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(FILE_INDEX, f)

    speak("Indexing complete")


def find_path(name):
    build_index()

    names = [item[0] for item in FILE_INDEX]
    matches = get_close_matches(name.lower(), names, n=1, cutoff=0.6)

    if matches:
        for n, full_path in FILE_INDEX:
            if n == matches[0]:
                return full_path

    return None


# 🔥 CLEAN TEXT
def clean_name(text):
    words = ["open", "my", "the", "folder", "app", "application"]
    text = text.lower()
    for w in words:
        text = text.replace(w, "")
    return text.strip()


def clean_google_query(text):
    words = ["search", "google", "find", "look up", "for"]
    text = text.lower()
    for w in words:
        text = text.replace(w, "")
    return text.strip()


def clean_youtube_query(text):
    words = ["play", "search", "on youtube", "youtube", "for"]
    text = text.lower()
    for w in words:
        text = text.replace(w, "")
    return text.strip()


def execute_action(command, raw_text=None):

    # 🎵 MUSIC
    if command == "music":
        speak("Opening Spotify")
        os.system("start spotify:")
        time.sleep(5)
        pyautogui.press("space")
        return True

    # 🌐 GOOGLE SEARCH
    elif command == "google_search":
        if raw_text:
            query = clean_google_query(raw_text)
            webbrowser.open(f"https://www.google.com/search?q={query}")
            speak(f"Searching {query}")
        return True

    # ▶ YOUTUBE SEARCH
    elif command == "youtube_search":
        if raw_text:
            query = clean_youtube_query(raw_text)
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
            speak(f"Searching YouTube for {query}")
        return True

    # 🔥 OPEN ANYTHING (FINAL UNIVERSAL FIX)
    elif command == "open_app":
        if raw_text:
            name = clean_name(raw_text)

            # ✅ STEP 1: SPECIAL APPS
            for key in SPECIAL_APPS:
                if key in name:
                    speak(f"Opening {key}")
                    os.system(f"start {SPECIAL_APPS[key]}")
                    return True

            # ✅ STEP 2: WINDOWS SHELL (VERY IMPORTANT)
            result = os.system(f'start "" {name}')
            if result == 0:
                speak(f"Opening {name}")
                return True

            # ✅ STEP 3: FILE / FOLDER
            path = find_path(name)
            if path:
                speak(f"Opening {name}")
                os.startfile(path)
                return True

            # 🌐 fallback
            webbrowser.open(f"https://www.google.com/search?q={name}")
            speak("Not found")

        return True

    # 🔊 VOLUME
    elif command == "volume_up":
        for _ in range(5):
            pyautogui.press("volumeup")
        speak("Volume increased")
        return True

    elif command == "volume_down":
        for _ in range(5):
            pyautogui.press("volumedown")
        speak("Volume decreased")
        return True

    elif command == "mute":
        pyautogui.press("volumemute")
        speak("Muted")
        return True

    # 📸 SCREENSHOT
    elif command == "screenshot":
        path = os.path.join(os.path.expanduser("~"), "Downloads",
                            f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        img = pyautogui.screenshot()
        img.save(path)
        speak("Screenshot saved")
        return True

    # 🕒 TIME
    elif command == "time":
        speak(datetime.now().strftime("%I:%M %p"))
        return True

    # ❌ EXIT
    elif command == "exit":
        speak("Goodbye")
        return False

    else:
        speak("I did not understand")
        return True