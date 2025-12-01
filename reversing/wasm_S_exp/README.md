# 題材とする脆弱性

WebAssemblyテキスト形式(S式)の可読性

# 実現するためのテーマ

WebAssemblyのスタックマシンへの理解を深める

# 想定する参加者が解答までに至る思考経路

1. Memoryの1024番地以降に格納されているデータがフラグの値と一致しているか1文字ずつ確認するコードだと理解する
2. インデックスと比較している値を使って、フラグ文字列を作成し表示する（他の言語 or WebAssembly + Javascript）

# 想定する難易度

Medium

# 参考資料

https://developer.mozilla.org/en-US/docs/WebAssembly/Reference
