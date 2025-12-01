# 題材とする脆弱性

stack pivot

# 実現するためのテーマ

0x10バイトのオーバーフローができるがone_gadgetが使えない状況下において、シェルを取れるようになる。
stackのアドレスやsystem関数を与えることで、stack pivotさえできれば解けるようにした。

# 想定する参加者が解答までに至る思考経路

read関数で0x10バイトのオーバーフローがあることに気がつく。
one_gadgetやwin関数がないので、return addressの書き換えのみではシェルを取れない。
saved rbpを書き換えできることから、`leave; ret`を利用してstack pivotする。

# 想定する難易度

Medium
