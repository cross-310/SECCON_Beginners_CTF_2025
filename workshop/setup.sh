#!/usr/bin/env bash
# Codespace 作成時(postCreateCommand)に1回だけ実行されるセットアップ。
# ngrok のインストールと Docker の確認を行う。
set -euo pipefail

echo "[setup] installing ngrok agent ..."
if ! command -v ngrok >/dev/null 2>&1; then
  curl -sSL https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz \
    | sudo tar -xz -C /usr/local/bin ngrok
fi
ngrok version || true

echo "[setup] docker check ..."
docker version >/dev/null 2>&1 && echo "[setup] docker OK" || echo "[setup] docker not ready yet (DinD 起動待ちの可能性)"

chmod +x workshop/*.sh || true

cat <<'MSG'

[setup] 完了しました。次の手順:
  1) ngrok の authtoken を登録（無料アカウントのダッシュボードから取得）
       export NGROK_AUTHTOKEN=xxxxxxxx
     ※ TCP エンドポイント利用にはクレジットカード認証が一度必要です。
  2) workshop/config.sh を編集して出題する問題を選ぶ
  3) bash workshop/up.sh で起動
MSG
