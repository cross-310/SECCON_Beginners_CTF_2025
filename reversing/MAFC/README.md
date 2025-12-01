# 題材とする脆弱性

疑似マルウェアの静的解析

# 実現するためのテーマ

AES-256にて暗号化されたファイルの復元

# 想定する参加者が解答までに至る思考経路

1. デコンパイラを使って解析を行う
2. 関数内の処理やstringsから`Microsoft Enhanced RSA and AES Cryptographic Provider`を用いて暗号化を行っていることを確認
3. 暗号化鍵並びにIVをstringsで定義しているものを使用していることも確認

# 想定する難易度

Hard

# 参考資料
- https://learn.microsoft.com/ja-jp/windows/win32/api/wincrypt/
- https://learn.microsoft.com/ja-jp/windows/win32/api/fileapi/
- https://www.trustss.co.jp/smnEasyEnc1E0.html
- https://wisdom.sakura.ne.jp/system/winapi/win32/win111.html
