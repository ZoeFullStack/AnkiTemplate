import requests
from datetime import datetime

# 这个代码可以遍历anki卡片然后修改指定的字段，去掉前面的 [sound:] 和后面的 ],hypertts生成的vdedio可以调整播放进度，如果前面有这些前缀，anki会自动解析为音频，导致无法调整播放
ANKI_CONNECT_URL = "http://127.0.0.1:8765"

# 可配置的变量
FIELD_NAME = "正面"  
DECK_NAME = "test-j"  
# FIELD_NAME = "VocabAudio"  
# DECK_NAME = "test-1" 
# 获取指定牌组中的所有卡片
def get_cards_by_deck(deck_name):
    payload = {
        "action": "findNotes",
        "version": 6,
        "params": {"query": f"deck:{deck_name}"}
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    if result.get("error") is None:
        return result.get("result", [])
    else:
        print("Error:", result.get("error"))
        return []

# 获取卡片的字段内容
def get_card_fields(note_id):
    payload = {"action": "notesInfo", "version": 6, "params": {"notes": [note_id]}}
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    if result.get("error") is None:
        # print(result["result"][0]["fields"])
        return result["result"][0]["fields"]
    else:
        print("Error:", result.get("error"))
        return {}


def fix_updated_fields(fields):
    return {key: value["value"] for key, value in fields.items()}


# 更新卡片的字段内容
def update_card(note_id, updated_content):
    payload = {
        "action": "updateNoteFields",
        "version": 6,
        "params": {
            "note": {
                "id": note_id,
                "fields": {
                    FIELD_NAME: updated_content  # 使用变量 FIELD_NAME
                },
            }
        },
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    print(result)


# 批量修改指定牌组中的卡片字段
def modify_cards_in_deck(deck_name):
    # 获取指定牌组中的所有卡片
    note_ids = get_cards_by_deck(deck_name)

    for note_id in note_ids:
        fields = get_card_fields(note_id)
        # 如果指定字段存在并且包含 [sound:xxx]，则进行修改
        if FIELD_NAME in fields:
            field_content = fields[FIELD_NAME]
            # 确保 field_content 是字典且包含 value 键
            if isinstance(field_content, dict) and "value" in field_content:
                field_value = field_content["value"]
                # 如果包含 sound:xxx 的格式，则修改为去掉前括号和 "sound:" 的内容
                if field_value.startswith("[sound:") and field_value.endswith("]"):
                    print(field_value)
                    print(fields)
                    new_content = field_value[7:-1]  # 去掉 "sound:" 和 "[ ]"
                    update_card(note_id, new_content)  # 更新卡片



if __name__ == "__main__":
    # 修改卡片字段
    print("正在修改卡片字段...")
    modify_cards_in_deck(DECK_NAME)