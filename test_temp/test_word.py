import requests
import json

# 这个代码可以遍历anki卡片然后修改指定的字段，去掉前面的 [sound:] 和后面的 ]，还可以统计出超过7次的good卡片
# AnkiConnect 地址
ANKI_CONNECT_URL = "http://127.0.0.1:8765"

# 可配置的变量
FIELD_NAME = "正面" 
DECK_NAME = "test-j" 

# FIELD_NAME = "VocabAudio"  
# DECK_NAME = "test-1" 


# 通过 AnkiConnect 获取指定牌组中的所有卡片
def get_cards_by_deck(deck_name):
    payload = {
        "action": "findNotes",
        "version": 6,
        "params": {"query": f"deck:{deck_name}"},  # 获取指定牌组中的所有卡片
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
        print(result["result"][0]["fields"])
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

    print(payload)  # 打印请求内容，确认字段和数据格式
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
                    new_content = field_value[7:-1]  # 去掉 "sound:" 和 "[ ]"
                    update_card(note_id, new_content)  # 更新卡片



# 获取卡片的复习记录
def get_reviews_of_cards(card_ids):
    payload = {
        "action": "getReviewsOfCards",
        "version": 6,
        "params": {"cards": card_ids}
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    if result.get("error") is None:
        # print("复习记录返回值:", json.dumps(result["result"], indent=4, ensure_ascii=False))  # 打印返回值
        return result["result"]
    else:
        print("Error:", result.get("error"))
        return {}

# 获取卡片的详细信息，包括 noteId 和字段内容
def get_card_info(card_id):
    payload = {
        "action": "cardsInfo",
        "version": 6,
        "params": {"cards": [card_id]}
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    if result.get("error") is None:
        return result["result"][0]  # 返回卡片的详细信息
    else:
        print("Error:", result.get("error"))
        return None

# 筛选点击 Good 超过 7 次的卡片
def filter_good_cards(deck_name, good_threshold=7):
    note_ids = get_cards_by_deck(deck_name)
    good_cards = []

    # 获取所有卡片的复习记录
    reviews = get_reviews_of_cards(note_ids)

    # 遍历复习记录，统计点击 "Good" 的次数
    for card_id, review_list in reviews.items():  # 遍历字典的键和值
        good_clicks = sum(1 for entry in review_list if entry["ease"] == 3)
        if good_clicks > good_threshold:
            good_cards.append(card_id)  # 添加 cardId 到结果列表

    return good_cards

if __name__ == "__main__":
    modify_cards_in_deck(DECK_NAME)
    good_cards = filter_good_cards(DECK_NAME, good_threshold=7)
    print("点击 Good 超过 7 次的卡片 ID:")
    for card_id in good_cards:
        print(card_id)
