import requests
import json
from datetime import datetime

# 这个代码可以遍历anki卡片然后修改指定的字段，去掉前面的 [sound:] 和后面的 ]，这个代码还会统计指定牌组中的复习good超过七次，并且上一次也是good，并且和上一次good不是同一天的，确定不是在同一天的复习成功超过七次，已经转换为长期记忆的卡片，转换成suspend
# AnkiConnect 地址
ANKI_CONNECT_URL = "http://127.0.0.1:8765"

# 可配置的变量
FIELD_NAME = "正面"  # 替换为你的字段名
DECK_NAME = "test-j"  # 替换为你的牌组名称
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
        return result["result"]
    else:
        print("Error:", result.get("error"))
        return {}

# 获取卡片的详细信息，包括 noteId
def get_card_info(card_ids):
    payload = {
        "action": "cardsInfo",
        "version": 6,
        "params": {"cards": card_ids}
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    if result.get("error") is None:
        return result["result"]  # 返回卡片的详细信息列表
    else:
        print("Error:", result.get("error"))
        return []

# 使用 areSuspended 方法筛选非暂停状态的卡片
def filter_non_suspended_cards(card_ids):
    payload = {
        "action": "areSuspended",
        "version": 6,
        "params": {"cards": card_ids}
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    if result.get("error") is None:
        suspended_status = result["result"]  # 返回一个布尔值列表
        non_suspended_cards = [
            card_id for card_id, is_suspended in zip(card_ids, suspended_status) if not is_suspended
        ]
        return non_suspended_cards
    else:
        print("Error:", result.get("error"))
        return []

# 将符合条件的卡片设置为暂停状态
def suspend_cards(card_ids):
    payload = {
        "action": "suspend",
        "version": 6,
        "params": {"cards": card_ids}
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    if result.get("error") is None:
        print(f"成功将以下卡片设置为暂停状态: {card_ids}")
    else:
        print("Error:", result.get("error"))

# 筛选点击 Good 超过 7 次的卡片，并输出 noteId
def filter_good_cards(deck_name, good_threshold=7):
    note_ids = get_cards_by_deck(deck_name)
    card_ids = list(map(int, note_ids))  # 确保 card_ids 是整数列表
    good_cards = []

    # 获取所有卡片的复习记录
    reviews = get_reviews_of_cards(card_ids)

    # 遍历复习记录，统计符合条件的 Good 次数
    for card_id, review_list in reviews.items():  # 遍历字典的键和值
        # 按时间排序复习记录
        review_list.sort(key=lambda x: x["id"])
        good_clicks = 0
        for i in range(1, len(review_list)):
            current_review = review_list[i]
            previous_review = review_list[i - 1]

            # 检查当前和上一次的复习是否都是 Good
            if current_review["ease"] == 3 and previous_review["ease"] == 3:
                # 检查是否是不同日期
                current_date = datetime.fromtimestamp(current_review["id"] / 1000).date()
                previous_date = datetime.fromtimestamp(previous_review["id"] / 1000).date()
                if current_date != previous_date:
                    good_clicks += 1

        # 如果符合条件的 Good 次数超过阈值，添加到结果列表
        if good_clicks > good_threshold:
            good_cards.append(int(card_id))  # 添加 cardId 到结果列表

    # 使用 areSuspended 方法检查卡片是否暂停
    non_suspended_cards = filter_non_suspended_cards(good_cards)

    # 获取这些卡片的详细信息以提取 noteId
    card_info_list = get_card_info(non_suspended_cards)
    good_notes = [card_info["note"] for card_info in card_info_list]

    return good_notes, non_suspended_cards

if __name__ == "__main__":
    # 修改卡片字段
    # print("正在修改卡片字段...")
    # modify_cards_in_deck(DECK_NAME)

    # 筛选点击 Good 超过 7 次的卡片
    print("正在筛选点击 Good 超过 7 次的卡片...")
    good_notes, good_card_ids = filter_good_cards(DECK_NAME, good_threshold=7)
    print("点击 Good 超过 7 次的 Note ID（非暂停状态）:")
    for note_id in good_notes:
        print(note_id)

    # 将符合条件的卡片设置为暂停状态
    print("正在将符合条件的卡片设置为暂停状态...")
    suspend_cards(good_card_ids)
