## 題材とする脆弱性

MySQLの暗黙的な型キャストによる認証バイパス

## 実現するためのテーマ

secret tokenの先頭に数字が入っていた場合、このように末尾の値が分からなくても一致させることができます。

* `SELECT "1751183148_53cr37_t0k3n" = 1751183148;`

ここで、先頭が推測可能(unix timestampなど)である場合、tokenが一致するような値を作成することができます。

## 想定する参加者が解答までに至る思考経路

1. adminの情報がseedとしてdbに入っていることに気づく
2. adminでログインできればフラグが手に入ることに気づく
3. パスワードリセット機能でトークンを持っていればadminのセッションを取得できることがわかる
4. `generateResetToken`関数で生成されたトークンの先頭が推測可能かつ`/api/reset-password`の`validateResetTokenByUsername`ではリセットトークンを使用して値が存在していればadminとして認証されることがわかる

## 想定する難易度

Hard

mediumでもいいですが、難化を緩和するためにHardにしてもいいかなとも思っています。

## 参考資料

* [Loose-Compare-Tables](https://github.com/Hakumarachi/Loose-Compare-Tables)