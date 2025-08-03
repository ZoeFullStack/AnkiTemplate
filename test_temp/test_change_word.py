from googletrans import Translator
import requests
import re
import time
import json
import os

ANKI_CONNECT_URL = "http://127.0.0.1:8765"
FIELD_NAME = "SentDef1"  # The field name to modify
# FIELD_NAME = "VocabDefCN"  # The field name to modify
DECK_NAME = "test-1"
TARGET_LANG = "en"
CACHE_FILE = "translation_cache.json"

# Load local cache
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        translation_cache = json.load(f)
else:
    translation_cache = {}

def save_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(translation_cache, f, ensure_ascii=False, indent=2)

def is_chinese(text):
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def get_cards_by_deck(deck_name):
    print(f"[DEBUG] Fetching note ids for deck: {deck_name}")
    payload = {
        "action": "findNotes",
        "version": 6,
        "params": {"query": f"deck:{deck_name}"}
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    if result.get("error") is None:
        print(f"[DEBUG] Found {len(result.get('result', []))} notes in deck '{deck_name}'")
        return result.get("result", [])
    else:
        print("Error:", result.get("error"))
        return []

def get_card_fields(note_id):
    print(f"[DEBUG] Fetching fields for note_id: {note_id}")
    payload = {"action": "notesInfo", "version": 6, "params": {"notes": [note_id]}}
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    if result.get("error") is None:
        return result["result"][0]["fields"]
    else:
        print("Error:", result.get("error"))
        return {}

def update_card(note_id, updated_content):
    print(f"[DEBUG] Updating note_id: {note_id} with new content.")
    payload = {
        "action": "updateNoteFields",
        "version": 6,
        "params": {
            "note": {
                "id": note_id,
                "fields": {
                    FIELD_NAME: updated_content
                },
            }
        },
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    print(f"[DEBUG] Update response: {response.json()}")

def mymemory_translate(text):
    print(f"[DEBUG] Translating: {text}")
    if text in translation_cache:
        print(f"[DEBUG] Cache hit for: {text}")
        return translation_cache[text]
    for attempt in range(3):  # Retry up to 3 times
        try:
            print(f"[DEBUG] MyMemory request attempt {attempt+1} for: {text}")
            resp = requests.get(
                "https://api.mymemory.translated.net/get",
                params={"q": text, "langpair": "zh|en"},
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json()
                translated = data.get("responseData", {}).get("translatedText", "")
                translation_cache[text] = translated
                save_cache()
                print(f"[DEBUG] Translated: {text} -> {translated}")
                time.sleep(1.5)  # Control request frequency
                return translated
            else:
                print(f"[DEBUG] MyMemory response status: {resp.status_code}")
        except Exception as e:
            print(f"MyMemory error for '{text}': {e}, retrying...")
            time.sleep(2)
    print(f"[DEBUG] Failed to translate: {text}")
    return ""

def modify_cards_in_deck(deck_name, batch_size=50):
    print(f"[DEBUG] Starting modify_cards_in_deck for deck: {deck_name}")
    note_ids = get_cards_by_deck(deck_name)
    batch = []
    batch_note_ids = []
    for idx, note_id in enumerate(note_ids):
        print(f"[DEBUG] Processing note {idx+1}/{len(note_ids)}: {note_id}")
        fields = get_card_fields(note_id)
        if FIELD_NAME in fields:
            field_content = fields[FIELD_NAME]
            if isinstance(field_content, dict) and "value" in field_content:
                field_value = field_content["value"]
                print(f"[DEBUG] Field value: '{field_value}'")
                if not field_value.strip():
                    print(f"[DEBUG] Skipped empty field for note_id: {note_id}")
                    continue
                if not is_chinese(field_value):
                    print(f"[DEBUG] Skipped non-Chinese field for note_id: {note_id}")
                    continue
                batch.append(field_value)
                batch_note_ids.append(note_id)
                if len(batch) == batch_size:
                    print(f"[DEBUG] Translating batch of {batch_size} items...")
                    translated_list = [mymemory_translate(text) for text in batch]
                    for nid, orig, trans in zip(batch_note_ids, batch, translated_list):
                        print(f"Original: {orig} -> Translated: {trans}")
                        update_card(nid, trans)
                    batch = []
                    batch_note_ids = []
    # Handle the last batch if less than batch_size
    if batch:
        print(f"[DEBUG] Translating final batch of {len(batch)} items...")
        translated_list = [mymemory_translate(text) for text in batch]
        for nid, orig, trans in zip(batch_note_ids, batch, translated_list):
            print(f"Original: {orig} -> Translated: {trans}")
            update_card(nid, trans)

if __name__ == "__main__":
    print("Translating and modifying cards in the deck...")
    modify_cards_in_deck(DECK_NAME, batch_size=50)