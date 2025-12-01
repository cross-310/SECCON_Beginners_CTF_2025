# skipping
## 題材とする脆弱性

特定のヘッダの信頼

## 実現するためのテーマ

`/flag`には通常のリクエストではアクセスできないが、`x-ctf4b-request`をヘッダを付与するとアクセスできるようにする。

## 想定する参加者が解答までに至る思考経路

1. `/flag` へのアクセスはブロックされることに気づく。
2. ソースコードを確認すると`x-ctf4b-request:ctf4b`をヘッダとして付与すればアクセスできることに気づく。

## 想定する難易度

Beginner

## 参考資料

https://github.com/advisories/GHSA-f82v-jwr5-mffw