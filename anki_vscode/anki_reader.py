import json
import requests
import time
import os

# 连接到 AnkiConnect（确保 Anki 运行时 AnkiConnect 插件已安装）
ANKI_CONNECT_URL = "http://127.0.0.1:8765"

def get_current_card():
    payload = {
        "action": "guiCurrentCard",
        "version": 6
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()

    if "result" in result and result["result"]:
        back_content = result["result"]["fields"]["Back"]["value"]
        return back_content
    else:
        return None

def clear_console():
    """清空控制台输出，适配 Windows 和 Unix 系统"""
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    while True:
        clear_console()  # 每次刷新前清空终端
        back_content = get_current_card()
        if back_content:
            print("\n当前卡片的背面内容：")
            print(back_content)
        else:
            print("未找到当前卡片")
        
        time.sleep(1)  # 每秒刷新一次
