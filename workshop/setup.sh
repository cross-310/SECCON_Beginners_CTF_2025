#!/usr/bin/env bash
# Codespace 作成時(postCreateCommand)に1回だけ実行されるセットアップ。
set -euo pipefail
echo "[setup] installing ngrok agent ..."
if ! command -v ngrok >/dev/null 2>&1; then
  curl -sSL https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz \
    | sudo tar -xz -C /usr/local/bin ngrok
fi
ngrok version || true
docker version >/dev/null 2>&1 && echo "[setup] docker OK" || echo "[setup] docker not ready yet"
chmod +x workshop/*.sh || true
cat <<'MSG'

[setup] 完了。次の手順:
  1) ngrok authtoken を登録: export NGROK_AUTHTOKEN=xxxxxxxx
     ※ TCP 利用には ngrok 側で一度クレジットカード認証が必要
  2) (推奨) bash workshop/replace-flags.sh  でフラグをダミー化
  3) bash workshop/up.sh                    で起動
MSG
