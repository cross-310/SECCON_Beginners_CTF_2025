# 題材とする脆弱性

Kernel ExploitにおけるTOCTOU

# 実現するためのテーマ

Kernel Pwnにおいて、TOCTOUの攻撃をできるようになる。
userfaultfdを利用して、Race Conditionを安定して発生させることができるようになる。
カーネルで任意アドレスへ書き込みできるとき、`modprobe_path`の書き換えなどの方法で権限昇格できるようになる。

# 想定する参加者が解答までに至る思考経路

ドライバのコードを読むと、ioctlでロックを何も取っていないことがわかるので、TOCTOUを疑う。
writeでoffsetのcheckが終わった後にseekを用いてoffsetを変更できることに気がつく。
kaslrがないのでleakは必要なく、modprobe_pathを書き換えれば良いことに気がつく。
Race Conditionを安定して発生させるためにuserfaultfdを利用する。

# 想定する難易度

Hard

# 参考資料

https://pawnyable.cafe/linux-kernel/LK04/uffd.html
https://p3land.smallkirby.com/kernel/uaf/#challenge%E6%A6%82%E8%A6%81%E3%81%A8toctou
