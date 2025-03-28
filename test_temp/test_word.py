import requests
import json

# AnkiConnect 地址
ANKI_CONNECT_URL = "http://127.0.0.1:8765"

# 通过 AnkiConnect 获取指定牌组中的所有卡片
def get_cards_by_deck(deck_name):
    payload = {
        "action": "findNotes",
        "version": 6,
        "params": {
            "query": f"deck:{deck_name}"  # 获取指定牌组中的所有卡片
        }
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    if result.get('error') is None:
        return result.get('result', [])
    else:
        print("Error:", result.get('error'))
        return []

# 获取卡片的字段内容
def get_card_fields(note_id):
    payload = {
        "action": "notesInfo",
        "version": 6,
        "params": {
            "notes": [note_id]
        }
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    if result.get('error') is None:
        return result['result'][0]['fields']
    else:
        print("Error:", result.get('error'))
        return {}

# 更新卡片的字段内容
def update_card(note_id, updated_fields):
    payload = {
        "action": "updateNotesFields",
        "version": 6,
        "params": {
            "notes": [{
                "noteId": note_id,
                "fields": updated_fields
            }]
        }
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    if result.get('error') is None:
        print(f"Updated note ID: {note_id}")
    else:
        print("Error:", result.get('error'))

# 批量修改指定牌组中的卡片字段
def modify_cards_in_deck(deck_name):
    # 获取指定牌组中的所有卡片
    note_ids = get_cards_by_deck(deck_name)
    
    for note_id in note_ids:
        fields = get_card_fields(note_id)
        
        # 如果 "正面" 字段存在并且包含 [sound:xxx]，则进行修改
        if "正面" in fields:
            front_content = fields["正面"]
            # 如果包含 sound:xxx 的格式，则修改为去掉前括号和 "sound:" 的内容
            if front_content.startswith("[sound:") and front_content.endswith("]"):
                new_content = front_content[7:-1]  # 去掉 "sound:" 和 "[ ]"
                fields["正面"] = new_content  # 更新字段内容
                update_card(note_id, fields)  # 更新卡片

if __name__ == "__main__":
    deck_name = "test-j"  # 需要修改的牌组名称
    modify_cards_in_deck(deck_name)
