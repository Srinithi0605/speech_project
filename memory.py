# memory.py

import csv
import os

LOG_FILE = "command_log.csv"
DATASET_FILE = "dataset.csv"


def log_command(user_text, predicted):
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["text", "prediction"])

        writer.writerow([user_text, predicted])


def save_correction(user_text, correct_label):
    file_exists = os.path.isfile(DATASET_FILE)

    with open(DATASET_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["text", "label"])

        writer.writerow([user_text, correct_label])