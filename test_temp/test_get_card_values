import requests

# 获取指定牌组中的指定多个字段，并且用逗号隔开，输出多个卡片行
# AnkiConnect 地址
ANKI_CONNECT_URL = "http://127.0.0.1:8765"

# 指定的牌组名称
DECK_NAME = "N1"  # 替换为实际牌组名称

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

# 获取卡片的详细信息
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

if __name__ == "__main__":
    # 获取牌组中的所有卡片
    card_ids = get_cards_by_deck(DECK_NAME)
    if not card_ids:
        print("未找到任何卡片")
        exit()

    # 获取卡片的详细信息
    card_info_list = get_card_info(card_ids)

    # 输出每个卡片的字段信息
    print("卡片字段信息（每行一个卡片，字段用英文逗号隔开）：")
    for card_info in card_info_list:
        # 提取需要的字段，例如 noteId、字段内容等
        word = card_info.get("fields").get("Word").get("value")
        explain1 = card_info.get("fields").get("Explain1").get("value")
        connectiveType1 = card_info.get("fields").get("ConnectiveType1").get("value")
        

        # 将字段用英文逗号隔开
        print(f"{word},{explain1},{connectiveType1}")