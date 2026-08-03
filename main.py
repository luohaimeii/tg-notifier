import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
from pyrogram import Client, filters

# 1. 网页健康响应（防止平台休眠）
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Userbot is running!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_web_server, daemon=True).start()

# 2. 从 Secrets 读取环境变量
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
BARK_KEY = os.environ.get("BARK_KEY")

def send_bark(title, content):
    """发送 Bark 推送通知"""
    url = f"https://api.day.app/{BARK_KEY}/{requests.utils.quote(title)}/{requests.utils.quote(content)}"
    try:
        res = requests.get(url, timeout=5)
        print(f"Bark 推送请求已发送，响应状态码: {res.status_code}")
    except Exception as e:
        print(f"Bark 推送失败: {e}")

# 初始化 Userbot 客户端
app = Client(
    "my_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# 3. 监听所有私聊消息 (filters.private)
@app.on_message(filters.private)
def handle_all_private_messages(client, message):
    # 忽略自己发给别人的消息
    if message.outgoing:
        return

    sender_name = message.from_user.first_name if message.from_user else "Telegram 用户"
    text_content = message.text or message.caption or "[收到非文字/图片/语音/文件消息]"
    
    print(f"收到私聊消息 -> 发送者: {sender_name} | 内容: {text_content}")
    send_bark(f"TG消息提醒: {sender_name}", text_content)

print("Userbot 全私聊监听服务已成功启动...")
app.run()
