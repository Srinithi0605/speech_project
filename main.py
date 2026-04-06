# main.py

import pickle
from scipy.sparse import hstack
from speech_input import get_voice
from actions import execute_action

WAKE_WORD = "hey jarvis"

# 🔥 LOAD BOTH MODELS (ENSEMBLE)
model_lr = pickle.load(open("model_lr.pkl", "rb"))
model_svc = pickle.load(open("model_svc.pkl", "rb"))

# 🔥 LOAD VECTORIZERS
word_vectorizer = pickle.load(open("word_vectorizer.pkl", "rb"))
char_vectorizer = pickle.load(open("char_vectorizer.pkl", "rb"))

print("🤖 Assistant is listening... Say 'Hey Jarvis'")

active = False

while True:
    command = get_voice()

    if command == "":
        continue

    command = command.lower()
    print("Heard:", command)

    # 🔥 WAKE WORD
    if not active:
        if WAKE_WORD in command:
            print("✅ Activated")
            active = True
        continue

    # 🔥 SLEEP MODE
    if "sleep" in command or "go to sleep" in command:
        print("😴 Going to sleep...")
        active = False
        continue

    print("You said:", command)

    # =====================================================
    # 🔥 RULE ENGINE (HIGH ACCURACY LAYER)
    # =====================================================

    if any(x in command for x in ["file explorer", "explorer"]):
        prediction = "open_app"

    elif "file manager" in command:
        prediction = "files"

    elif any(x in command for x in [
        "settings", "control panel", "task manager",
        "spotify", "whatsapp", "photos", "camera"
    ]):
        prediction = "open_app"

    elif any(x in command for x in [
        "downloads", "documents", "desktop"
    ]):
        prediction = "files"

    elif "volume" in command:
        if "up" in command or "increase" in command:
            prediction = "volume_up"
        elif "down" in command or "decrease" in command:
            prediction = "volume_down"
        else:
            prediction = "volume_up"

    elif "mute" in command:
        prediction = "mute"

    elif "screenshot" in command:
        prediction = "screenshot"

    elif "time" in command:
        prediction = "time"

    elif "youtube" in command:
        prediction = "youtube_search"

    elif "google" in command or "search" in command:
        prediction = "google_search"

    else:
        # =====================================================
        # 🔮 ML ENSEMBLE (FINAL PREDICTION)
        # =====================================================

        X = hstack([
            word_vectorizer.transform([command]),
            char_vectorizer.transform([command])
        ])

        pred_lr = model_lr.predict(X)[0]
        pred_svc = model_svc.predict(X)[0]

        # 🔥 ENSEMBLE DECISION
        if pred_lr == pred_svc:
            prediction = pred_lr
        else:
            prediction = pred_lr  # Logistic is more stable

    print("Final command:", prediction)

    # 🔥 EXECUTE ACTION
    run = execute_action(prediction, command)

    if not run:
        break