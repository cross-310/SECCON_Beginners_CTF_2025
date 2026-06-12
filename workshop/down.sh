#!/usr/bin/env bash
# 全チャレンジと ngrok を停止。勉強会終了後に必ず実行（無料枠の消費を止める）。
set -euo pipefail
cd "$(dirname "$0")/.."
source workshop/config.sh
echo "==> ngrok を停止"; pkill -f "ngrok start" 2>/dev/null || true
echo "==> コンテナを停止"
for entry in "${CHALLENGES[@]}"; do
  IFS='|' read -r type name dir port <<< "$entry"
  [ -z "${dir:-}" ] && continue
  [ -d "$dir" ] && ( cd "$dir" && COMPOSE_PROJECT_NAME="$name" PORT="$port" docker compose down ) || true
done
echo "==> 完了。Codespace 自体も github.com/codespaces で停止/削除すること。"
