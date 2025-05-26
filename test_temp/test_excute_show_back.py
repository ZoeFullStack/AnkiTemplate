import json
import requests
import time
import os

# 连接到 AnkiConnect（确保 Anki 运行时 AnkiConnect 插件已安装）
ANKI_CONNECT_URL = "http://127.0.0.1:8765"

def get_current_card():
    """获取当前正在学习的卡片信息"""
    payload = {
        "action": "guiCurrentCard",
        "version": 6
    }
    try:
        response = requests.post(ANKI_CONNECT_URL, json=payload)
        response.raise_for_status()  # 检查 HTTP 请求是否成功
        result = response.json()

        if "result" in result and result["result"]:
            return result["result"]  # 返回完整的卡片信息
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to AnkiConnect: {e}")
        return None

def clear_console():
    """清空控制台输出，适配 Windows 和 Unix 系统"""
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    last_card_id = None  # 用于存储上一次的卡片 ID
    while True:
        current_card = get_current_card()
        if current_card:
            current_card_id = current_card.get("cardId")  # 获取当前卡片的唯一 ID
            if current_card_id != last_card_id:  # 如果卡片 ID 发生变化
                last_card_id = current_card_id
                clear_console()  # 清空终端

                # 判断 "背面" 是否有值
                back_value = current_card.get("fields", {}).get("背面", {}).get("value")
                sentence = current_card.get("fields", {}).get("sentence", {}).get("value")
                VocabKanji = current_card.get("fields", {}).get("VocabKanji", {}).get("value")
                Example1 = current_card.get("fields", {}).get("Example1", {}).get("value")
                meaning = current_card.get("fields", {}).get("meaning", {}).get("value")
                output = ""
                if back_value:  # 如果 "背面" 有值
                    output += back_value

                if sentence:  # 如果 "sentence" 有值
                    output += sentence
                
                elif VocabKanji: 
                    output = (
                        current_card.get("fields", {}).get("VocabKanji", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("VocabDefCN", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("SentFurigana1", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("SentDef1", {}).get("value", "")
                    )
                    print(output)  # 直接打印字符串，保留换行效果
                elif meaning:
                    output = (
                        current_card.get("fields", {}).get("grammer", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("connect", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("sentence", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("meaning", {}).get("value", "")
                    )
                    print(output) 
                elif Example1:
                    output = (
                        current_card.get("fields", {}).get("Word", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("Explain1", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("Chinese1", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("Example1", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("Chinese1", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("Example2", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("Chinese2", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("Example3", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("Chinese3", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("Example4", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("Chinese4", {}).get("value", "") 
                    )
                    print(output)  
                print(json.dumps(output, ensure_ascii=False, indent=4))
        else:
            print("can't find this test")

        time.sleep(0.5)
