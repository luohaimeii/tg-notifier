import os
import requests
from pyrogram import Client, filters

# 从环境变量中读取配置
API_ID = int(os.environ.get("39325853"))
API_HASH = os.environ.get("009d2f87fb20e832e5226f017051d782")
SESSION_STRING = os.environ.get("BQJYEJ0ATap0h19HesgMed889P-A1LwIi8X8KUh0zkAVuDCHralJsHx1Z4SPZqgo6wwLv93-vSMko-E_lCPHU1K5KS1QzpCKAua1szDtMEq0vcuxz6fRE_OxagmAXC5vSHbxDCbqxpQI8rTfB42IlrSHT2plDbiAfOqp6UU7_kC6eTpewCHO3ZcmNA0Wh_h3wTSIRvCL9BUani3XhhD8Dea9WOGmMnoSuaU-0HReZ16vfevS4ygJps4rANR6jiI5aU5cpYDOn5GPT-2hu8yqIMZlHhZvRelNKoxhD_w4fyhvwF9QcAZ0kOkJfeovoTLzP1q59DG-lL_4opYtGwAp5W6olAQlogAAAAHTBUm_AA")
TARGET_USER = os.environ.get("hxckefuAA")  # 支持数字 ID 或字符串用户名 (如 HelloBeck)
BARK_KEY = os.environ.get("UnxHHRdAZDq8r8ChWnWaTg")

# 如果输入的 TARGET_USER 是纯数字，自动转换为 int
if TARGET_USER and TARGET_USER.isdigit():
    TARGET_USER = int(TARGET_USER)

def send_bark(title, content):
    """发送 Bark 推送通知"""
    url = f"https://api.day.app/{BARK_KEY}/{requests.utils.quote(title)}/{requests.utils.quote(content)}"
    try:
        requests.get(url, timeout=5)
    except Exception as e:
        print(f"Bark 推送失败: {e}")

# 初始化 Userbot 客户端
app = Client(
    "my_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# 监听特定用户的私聊消息
@app.on_message(filters.private & filters.user(TARGET_USER))
def handle_target_message(client, message):
    sender_name = message.from_user.first_name if message.from_user else "特定联系人"
    text_content = message.text or message.caption or "[收到图片/语音/文件/表情]"
    
    print(f"收到目标消息: {text_content}")
    send_bark(f"TG特待提醒: {sender_name}", text_content)

print("Userbot 监听服务已成功启动...")
app.run()
