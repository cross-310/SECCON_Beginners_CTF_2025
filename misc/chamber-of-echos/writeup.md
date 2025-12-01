# Writeup

## 概要
問題サーバは ICMP コバートチャネル攻撃により ICMP Echo Reply ペイロードからデータを外部送信するようになっています
また、送信されているデータは `0x546869734973415365637265744b6579` (= "ThisIsASecretKey") で AES-128-ECB + PKCS#7 Padding にて暗号化されています  

## 想定解法
1. ping コマンドなどでサーバーに何度か ICMP Echo Request を送信
1. ICMP Echo Reply のパケットをキャプチャ
1. ペイロード部分（暗号化された16バイト）を複数収集
1. 付属のキーで復号：

```python
# pycryptodome==3.23.0
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

KEY = b"546869734973415365637265744b6579"  # 16進数のキー
BLOCK_SIZE = 16  # AES-128-ECB のブロックサイズは 16bytes

key = bytes.fromhex(KEY.decode("utf-8"))
cipher = AES.new(key, AES.MODE_ECB)

for chunk in encrypted_blocks:
  print(unpad(cipher.decrypt(chunk), BLOCK_SIZE))
```
