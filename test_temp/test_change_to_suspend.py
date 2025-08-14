import requests
from datetime import datetime

# AnkiConnect 地址
ANKI_CONNECT_URL = "http://127.0.0.1:8765"

# 可配置的变量（多个牌组名称）
DECK_NAMES = ["test-j", "test-1", "test-note", "N1-2"]

# 获取指定牌组中的所有卡片
def get_cards_by_deck(deck_name):
    payload = {
        "action": "findCards",
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
        print(f"成功将以下卡片设置为暂停状态，CardId: {card_ids}")
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
    for deck_name in DECK_NAMES:
        print(f"process test: {deck_name}")
        
        # 筛选点击 Good 超过 7 次的卡片
        print("filtering...")
        good_notes, good_card_ids = filter_good_cards(deck_name, good_threshold=7)
        print("over 7 times node id:")
        for note_id in good_notes:
            print(note_id)

        # 将符合条件的卡片设置为暂停状态
        print("suspending cards...")
        suspend_cards(good_card_ids)
