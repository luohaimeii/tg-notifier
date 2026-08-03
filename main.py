import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
from pyrogram import Client, filters

# 1. 创建一个极简的 Web 服务，用于给 Render 健康检查
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Userbot is running!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# 后台开启 Web 监听
threading.Thread(target=run_web_server, daemon=True).start()

# 2. 从环境变量中读取配置
API_ID = int(os.environ.get("39325853"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("009d2f87fb20e832e5226f017051d782")
TARGET_USER = os.environ.get("hxckefuAA")  # 支持数字 ID 或字符串用户名 (如 HelloBeck)
BARK_KEY = os.environ.get("UnxHHRdAZDq8r8ChWnWaTg")

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
