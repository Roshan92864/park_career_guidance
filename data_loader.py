#utils/data_loader.py

import json
import os

BASE_PATH = os.path.join(os.path.dirname(__file__), "..", "data")

def load_json(filename):
    with open(os.path.join(BASE_PATH, filename), "r") as f:
        return json.load(f)

