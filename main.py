# main.py

import pickle
from speech_input import get_voice
from actions import execute_action

WAKE_WORD = "hey jarvis"

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

print("🤖 Assistant is listening... Say 'Hey Jarvis'")

active = False

while True:
    command = get_voice()

    if command == "":
        continue

    command = command.lower()
    print("Heard:", command)

    # 🔥 WAKE WORD DETECTION
    if not active:
        if WAKE_WORD in command:
            print("✅ Activated")
            active = True
        continue

    # 🔥 EXIT WAKE MODE
    if "sleep" in command or "go to sleep" in command:
        print("😴 Going to sleep...")
        active = False
        continue

    print("You said:", command)

    # 🔮 ML prediction
    X_test = vectorizer.transform([command])
    prediction = model.predict(X_test)[0]

    # 🔥 minimal fallback (keep system stable)
    if "mute" in command:
        prediction = "mute"

    elif "volume" in command:
        if "up" in command:
            prediction = "volume_up"
        elif "down" in command:
            prediction = "volume_down"

    elif "open" in command:
        prediction = "open_app"

    elif "screenshot" in command:
        prediction = "screenshot"

    elif "time" in command:
        prediction = "time"

    print("Final command:", prediction)

    # Execute action
    run = execute_action(prediction, command)

    if not run:
        break