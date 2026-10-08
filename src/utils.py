import os
import json
from src.config import OUTPUT_DIR


def save_json(name, data):
    with open(os.path.join(OUTPUT_DIR, name), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)