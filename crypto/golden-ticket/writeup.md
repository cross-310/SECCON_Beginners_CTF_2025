最初に`Get ticket`からchallengeを取得する。
`b"\x10"*16`を平文として暗号化すると、paddingによって`b"\x10"*32`が暗号化され、`xor(b"\x10"*16, d[:16], d[16:])`として`iv`を求めることができる。これを使うとAES_ECBとしての暗号化/復号オラクルが得られる。
`b"\x10"*16`を暗号文の3ブロック目として固定すると、encryptオラクルとdecryptオラクルを使ってそれぞれ後ろ/前の暗号文ブロックとして使うべき値を計算することができる。
これを使うと5回の追加のオラクル呼び出しで暗号文全体を計算することができ、golden ticketを得ることができる。

```python
f3 = b"\x10"*16
d = dec_oracle(f3)
iv = xor(b"\x10"*16, d[:16], d[16:])
f2 = xor(f3, d[16:], chal[2])
f1 = xor(dec_oracle(f2)[:16], iv, chal[1])
f0 = xor(dec_oracle(f1)[:16], iv, chal[0])
f4 = enc_oracle(xor(f3, iv, chal[3]))[:16]
f5 = enc_oracle(xor(f4, iv, chal[4]))[:16]
f6 = enc_oracle(xor(f5, iv, chal[5]))[:16]

get_ticket(f0+f1+f2+f3+f4+f5+f6)
```
