#!/usr/bin/env python3.12
import time
from re import match

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from scapy.all import *

type EncryptedChunk = bytes
type PlainChunk = bytes
type FlagText = str

################################################################################
KEY = b"546869734973415365637265744b6579"  # 16進数のキー
BLOCK_SIZE = 16  # AES-128-ECB のブロックサイズは 16bytes
################################################################################

def decode_key(key: bytes) -> bytes:
  """16進数のキーをバイト列に変換"""
  return bytes.fromhex(key.decode("utf-8"))

if __name__ == "__main__":
  from sys import argv
  server = argv[1] if (1 < len(argv)) else "127.0.0.1"
  print(f"[*] Connecting to {server}")

  cipher = AES.new(decode_key(KEY), AES.MODE_ECB)
  chunks = dict()

  while True:
    # ICMP Echo Request を送信
    pkt = IP(dst=server)/ICMP()
    reply = sr1(pkt, timeout=1, verbose=0)

    if not (reply and (Raw in reply)):
      continue

    chunk: EncryptedChunk = reply[Raw].load
    decrypted: PlainChunk = unpad(cipher.decrypt(chunk), BLOCK_SIZE)

    if m := re.match(rb"(\d+)\|(.+)", decrypted):
      idx = int(m.group(1))
      data = m.group(2).decode(errors="ignore")

      if idx in chunks:
        # 同じインデックスのチャンクが既にある場合はスキップ
        continue

      chunks[idx] = data
      print(f"[+] Got chunk {idx}: {data}")

      if 3 <= len(chunks):
        # ３チャンク分あればフラグは完成
        break

    time.sleep(0.8)  # サーバへの負荷を避けるために少し待つ

  # チャンクをインデックス順に並べてフラグを復元
  flag: FlagText = "".join(chunks[i] for i in sorted(chunks))
  print(flag)
