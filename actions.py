# actions.py

import webbrowser
import datetime
import os
import time
import json
import pyautogui
import pyttsx3
from difflib import get_close_matches

engine = pyttsx3.init()

FILE_INDEX = []
INDEX_FILE = "file_index.json"


def speak(text):
    print("🤖", text)
    engine.say(text)
    engine.runAndWait()


def clean_query(text, words_to_remove):
    text = text.lower()
    for word in words_to_remove:
        text = text.replace(word, "")
    return text.strip()


# 🔥 BUILD INDEX (ONE TIME)
def build_index():
    global FILE_INDEX

    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            FILE_INDEX = json.load(f)
        return

    speak("Indexing files, please wait")

    for root, dirs, files in os.walk("C:\\Users"):  # faster than full C
        for name in dirs + files:
            FILE_INDEX.append((name.lower(), os.path.join(root, name)))

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(FILE_INDEX, f)

    speak("Indexing complete")


def find_path(name):
    build_index()

    names = [item[0] for item in FILE_INDEX]
    matches = get_close_matches(name.lower(), names, n=1, cutoff=0.4)

    if matches:
        for n, full_path in FILE_INDEX:
            if n == matches[0]:
                return full_path

    return None


def find_app(app_name):
    start_menu_paths = [
        r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
        os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs")
    ]

    app_list = []

    for path in start_menu_paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".lnk"):
                    app_list.append((file.lower(), os.path.join(root, file)))

    names = [app[0] for app in app_list]
    matches = get_close_matches(app_name, names, n=1, cutoff=0.4)

    if matches:
        for name, full_path in app_list:
            if name == matches[0]:
                return full_path

    return None


def execute_action(command, raw_text=None):

    # 🎵 MUSIC
    if command == "music":
        speak("Opening Spotify")
        try:
            os.system("start spotify")
            time.sleep(5)
            pyautogui.press("space")
        except Exception as e:
            print("❌ Error:", e)
        return True

    # 🌐 GOOGLE
    elif command == "google":
        webbrowser.open("https://www.google.com")
        speak("Opening Google")
        return True

    # ▶ YOUTUBE
    elif command == "youtube":
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")
        return True

    # 🔥 OPEN ANYTHING (FIXED)
    elif command == "open_app":
        if raw_text:
            text = raw_text.lower()
            name = text.replace("open", "").replace("folder", "").strip()

            speak("Opening")

            try:
                # ✅ 1. APP FIRST
                app_path = find_app(name)
                if app_path:
                    os.startfile(app_path)
                    return True

                # ✅ 2. SYSTEM
                result = os.system(f'start "" "{name}"')
                if result == 0:
                    return True

                # ✅ 3. FILE/FOLDER
                path = find_path(name)
                if path:
                    os.startfile(path)
                    return True

            except Exception:
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

    # 🔋 SYSTEM
    elif command == "shutdown":
        speak("Shutting down")
        os.system("shutdown /s /t 1")
        return False

    elif command == "restart":
        speak("Restarting")
        os.system("shutdown /r /t 1")
        return False

    elif command == "lock":
        speak("Locking system")
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return True

    # 📸 SCREENSHOT
    elif command == "screenshot":
        from datetime import datetime

        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        full_path = os.path.join(downloads_path, filename)

        screenshot = pyautogui.screenshot()
        screenshot.save(full_path)

        speak("Screenshot taken and saved in downloads")
        return True

    # 🕒 TIME
    elif command == "time":
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
        return True

    # ❌ EXIT
    elif command == "exit":
        speak("Goodbye")
        return False

    else:
        speak("I did not understand that")
        return True