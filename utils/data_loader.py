#utils/data_loader.py

import json
import os

BASE_PATH = os.path.join(os.path.dirname(__file__), "..", "data")

def load_json(filename):
    path = os.path.join(BASE_PATH, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(filename, data):
    path = os.path.join(BASE_PATH, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
