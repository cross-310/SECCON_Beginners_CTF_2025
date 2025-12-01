# メモRAG
## 題材とする脆弱性
function callingにおける認可不備

## 実現するためのテーマ
RAG機能を持つメモアプリ. メモのアプリは`public`, `private`, `secret`の3種類.
- `public`: 誰でも閲覧可能
- `private`: 本人のみ閲覧可能
- `secret`: 本人のみ、パスワードを知っていれば閲覧可能

以下2つのtoolが定義されている.
- `search_memos`: メモを検索するためのtool. `target_uid`で検索対象のユーザーを指定することができる. `include_secret`を`true`にすると`secret`メモもコンテキストに加えることができる.
- `get_author_by_body`: メモの内容を元に誰が作成したかを調べることができる.

フラグはadminによって`secret`のメモとして保存されている. 

`get_author_by_body`を用いてフラグのメモの作成者を検索し, `search_memos`を用いてフラグのメモの内容を取得する.

## 想定する参加者が解答までに至る思考経路
1. ソースコードを読んで2つのtoolが定義されていることに気づく.
2. `get_author_by_body`でフラグのメモの作成者のIDを取得する.
3. `search_memos`でフラグのメモの内容を取得する.

## 想定する難易度
Medium

## 参考資料
https://platform.openai.com/docs/guides/function-calling