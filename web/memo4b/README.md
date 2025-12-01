# 題材とする脆弱性

URLパースを起因としたXSSの脆弱性。異なるURLパーサー(WHATWG URLとurl-parse)を組み合わせて使用することで、フラグメント部分(#)の処理の違いを悪用したXSS攻撃が可能。

# 実現するためのテーマ

シンプルなメモ共有アプリケーションに絵文字機能を実装。`:smile:`のような通常の絵文字に加え、`:https://example.com/image.png:`のようにURLを指定すると画像として表示できる。この際、URLの正規化にWHATWG URLを使い、フラグメント部分の取得にurl-parseを使うことで、imgタグに任意のパラメータを付与できる。

# 想定する参加者が解答までに至る思考経路

1. メモアプリケーションにアクセスし、問題文より絵文字機能を試す
2. URL絵文字機能（`:https://...:`）に気づき、画像が表示されることを確認する
3. ソースコードを確認し、2つの異なるURLライブラリが使われていることを発見する
4. url-parseがフラグメント内の特殊文字（特に`"`）をエンコードしないことに気づく
5. `:https://example.com/x.jpg#" onerror="alert(document.domain)":`のようなペイロードでXSSが可能であることを発見
6. 管理者ボットを使ってflagを外部に送信するペイロードを作成
7. このときにコロン(:)を含むと上手く動作しないので、Base64等を使って回避する

# 想定する難易度

medium

# 参考資料

- [url-parse - npm](https://www.npmjs.com/package/url-parse)
- [WHATWG URL Standard](https://url.spec.whatwg.org/)