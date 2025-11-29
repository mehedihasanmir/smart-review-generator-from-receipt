import json
import os
from typing import Dict, Any

def load_receipt_data(json_path: str) -> Dict[str, Any]:
    """Load receipt data from JSON file"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f" Error: Receipt JSON file not found at {json_path}")
        raise
    except json.JSONDecodeError:
        print(f" Error: Invalid JSON format in {json_path}")
        raise

def load_review_history(history_path: str = "review_history.json") -> Dict[str, Any]:
    """Load review history to check for duplicates"""
    if os.path.exists(history_path):
        try:
            with open(history_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"reviews": []}
    return {"reviews": []}

def save_review_history(history: Dict[str, Any], history_path: str = "review_history.json"):
    """Save updated review history"""
    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)