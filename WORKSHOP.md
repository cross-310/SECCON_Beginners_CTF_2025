# SECCON Beginners CTF 2025 勉強会 セットアップ手順（5問構成）

Codespaces を1台のホストにして、web 系は Codespaces のポート転送、
生TCP 系（pwnable / crypto の対話問題）は ngrok で公開する構成です。

## 出題する5問（確定）

| 問題 | カテゴリ | 種別 | ディレクトリ | ホストポート | フラグの埋め込み方 |
|---|---|---|---|---|---|
| kingyo_sukui | misc | web | `misc/kingyo_sukui/build` | 33333 | 静的ファイル（script.js 等）に埋め込み |
| skipping | web | web | `web/skipping/build` | 33455 | compose の `FLAG=` 環境変数 |
| log_viewer | web | web | `web/log_viewer/build` | 9999 | compose の `-flag=` 起動引数 |
| 01-translator | crypto | tcp | `crypto/01-translator/build` | 9001 (※) | compose の `FLAG=` 環境変数 |
| pet_name | pwnable | tcp | `pwnable/pet_name/build` | 9080 | `flag.txt` ファイル |

- web 3問は Codespaces 転送のみ（ngrok を消費しない）。
- tcp 2問だけ ngrok を使用（無料の同時3エンドポイント以内）。
- ※ 01-translator は元 compose が 9999 を使い log_viewer と衝突するため、
  `PORT=9001` に逃がしている。`up.sh` が自動で `PORT` を渡すので手動操作は不要。

---

## 0. 事前準備（一度だけ）

1. 対象リポジトリを自分のアカウントに **Fork**（元はアーカイブ済み read-only）。
   - ライセンス CC BY-NC-ND 4.0。改変 compose やイメージの **公開再配布は避ける**。
2. この `ctf-workshop` 配下（`.devcontainer/` と `workshop/`）を
   Fork したリポジトリの **ルート**に置いてコミット。
3. ngrok 無料アカウントを作成し authtoken を控える。
   - **TCP 利用にはクレジットカード認証が一度だけ必要**（課金はされない）。

すべてブラウザだけで完結します（ローカルインストール不要）。

---

## 1. Codespace を起動

Fork の `Code` ▶ `Codespaces` ▶ `Create codespace on main`。
2-core でよい（1時間なら無料枠 120 コア時間で十分）。
初回に `postCreateCommand`（`workshop/setup.sh`）で ngrok が自動導入される。

---

## 2. （推奨）フラグをダミー化

元リポジトリには本物のフラグが平文で入っている。出題前に置き換える。

```bash
bash workshop/replace-flags.sh
```

ただし**自動置換できるのは `flag.txt` 型（pet_name のみ）**。
残り4問は埋め込み方が異なるため、上表「フラグの埋め込み方」に従い手動で書き換える:

- skipping  : `web/skipping/build/compose.yml` の `FLAG: ctf4b{...}` を編集
- log_viewer: `web/log_viewer/build/compose.yml` の `-flag=ctf4b{...}` を編集
- 01-translator: `crypto/01-translator/build/compose.yml` の `- FLAG=ctf4b{...}` を編集
- kingyo_sukui: `misc/kingyo_sukui/build/` 配下の静的ファイル内のフラグを編集

> 勉強会で「フラグを伏せて解かせる」なら必須。答え合わせ用に本物を残すなら任意。

---

## 3. 起動

```bash
export NGROK_AUTHTOKEN=xxxxxxxx   # ngrok ダッシュボードの authtoken
bash workshop/up.sh
```

実行後、接続情報が表示される（例）:

```
[ web 系 ] ブラウザで開く
  - kingyo_sukui : https://<codespace>-33333.app.github.dev
  - skipping     : https://<codespace>-33455.app.github.dev
  - log_viewer   : https://<codespace>-9999.app.github.dev
[ tcp 系 ] nc で接続
  - 01-translator : nc 0.tcp.ngrok.io 12345
  - pet_name      : nc 0.tcp.ngrok.io 23456
```

---

## 4. web ポートを Public にする（手動・重要）

Codespaces の転送ポートは初期状態 **Private**（本人のみ）。参加者がアクセスできるよう Public にする:

- 画面下の **Ports** タブを開く
- 対象3ポート（33333 / 33455 / 9999）を右クリック ▶ **Port Visibility** ▶ **Public**

> Public にすると URL を知る誰でも無認証でアクセス可能。勉強会中だけにし、
> 終了後は Private に戻すか Codespace を停止すること。
> tcp 系（ngrok）はこの操作は不要。表示された `nc host port` をそのまま共有する。

---

## 5. 終了

```bash
bash workshop/down.sh
```

その後、**Codespace 自体も停止または削除**する（github.com/codespaces）。
忘れると無料コア時間を消費し続ける。

---

## 既知の制約・注意

- ngrok 無料: 同時3エンドポイント / 転送1GB / TCP接続5,000・月。今回 tcp は2本なので余裕。
- ngrok の interstitial（警告ページ）はブラウザHTTP向けで、nc/TCP には影響しない。
- Codespaces のポート転送 URL は HTTP/HTTPS のみ。生TCP は ngrok 経由。
- 参加者側: web 問題はブラウザのみで解けるが、tcp 問題（01-translator, pet_name）は
  手元に `nc` 等が必要。事前に共有しておくこと。
- 無料マシンは 2-core/8GB。5問同時起動は問題ないが、増やす場合はメモリに注意。
