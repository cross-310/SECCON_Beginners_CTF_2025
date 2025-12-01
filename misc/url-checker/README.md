# url-checker
## 題材とする脆弱性

URLの検証不備

## 実現するためのテーマ

URLのhostnameが先頭一致で検証されるので, `//[allowed_hostname].attacker.com`などで回避.

## 想定する参加者が解答までに至る思考経路

1. URLを入力できることに気づく.
2. 入力したURLが`urlparse`でパースされることに気づく.
3. パースされたURLのhostnameの先頭が`example.com`であればflagが得られることに気づく.
4. `//example.com.attacker.com`を入力してflagを得る.

## 想定する難易度

Easy

## 参考資料
