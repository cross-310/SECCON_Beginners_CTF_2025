# 題材とする脆弱性

EnumSystemLocales関数によるコードインジェクション

# 実現するためのテーマ

Windows向けのシェルコードを読めるようになる

# 想定する参加者が解答までに至る思考経路

1. UuidFromString関数等によって、UUID化されたシェルコードをデコードする
2. シェルコードを逆アセンブリしてソースコードを読む
3. TEBやPEBの構造を理解しながらフラグが表示される条件を探し出す

# 想定する難易度

Hard

# 参考資料

https://www.geoffchappell.com/studies/windows/km/ntoskrnl/inc/api/pebteb/rtl_user_process_parameters.htm
