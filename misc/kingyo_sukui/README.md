## 題材とする脆弱性

HTTP レスポンスの JavaScript は読める

## 実現するためのテーマ

HTTP レスポンスの JavaScript を読む

## 想定する参加者が解答までに至る思考経路

1. ゲームでは正しい順序で文字を選択すると、フラグが取れそうということがわかる
2. response の JS に`this.encryptedFlag`と`this.secretKey`があることがわかる
3. `decryptFlag()`関数があるので、それらを使ってフラグを復号する

## 想定する難易度

Beginner

## 参考資料
