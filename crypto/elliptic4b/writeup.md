まずは与えられたy座標を持つ楕円曲線上の点を計算する必要があります。
secp256k1という楕円曲線上の点は$y^2 = x^3 + 7$という関係式を満たすため、$x^3 = y^2-7$となるように$x$を選べばよいです。これには$\bmod p$上での$y^2-7$の3乗根を計算すればよいです。
次に`Q = a P`が`P.x == Q.x`かつ`P.y != Q.y`を満たす点となるような`a`を求めたいです。
このような点とは`P`の逆元にほかなりません。`P`の逆元とはつまり`P`を`-1`倍した点ですが、`a`は負にできません。そのため、代わりに`q-1`倍とすればよいです。これですべての条件を満たし、フラグが得られます。

```python
import os
from pwn import *
from sympy.ntheory.residue_ntheory import nthroot_mod
from fastecdsa.curve import secp256k1
from fastecdsa.point import Point

HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", "9999"))
sc = remote(HOST, PORT)

sc.recvuntil(b"y = ")
y = int(sc.recvline())
x = nthroot_mod(y**2 - 7, 3, secp256k1.p)
sc.recvuntil(b"x = ")
sc.sendline(str(x).encode())
sc.recvuntil(b"a = ")
a = secp256k1.q - 1
sc.sendline(str(a).encode())
print(sc.recvline())
```