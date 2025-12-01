# url-checker2
## 題材とする脆弱性

URLの検証不備

## 実現するためのテーマ

URLがport除去のため`:`でsplitされて先頭のものが検証に使用される.
また, hostnameが先頭一致で検証されるため, `//[allowd_hostname]:pass@[allowd_hostname].attacker.com`などで回避.

## 想定する参加者が解答までに至る思考経路

1. URLを入力できることに気づく.
2. 入力したURLが`urlparse`でパースされることに気づく.
3. URL内に`:`が使用される場合, `:`でsplitして先頭のものが検証に使用される. 先頭のものが`example.com`に完全一致することが必要.
4. 3に加えてURLのhostnameの先頭が`example.com`であればflagが得られることに気づく.
4. `//example.com:pass@example.com.attacker.com`を入力してflagを得る.

## 想定する難易度

Medium

## 参考資料
https://github.com/browser-use/browser-use/security/advisories/GHSA-x39x-9qw5-ghrf