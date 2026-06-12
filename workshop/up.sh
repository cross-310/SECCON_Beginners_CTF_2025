#!/usr/bin/env bash
# =============================================================================
# 5問を一括起動し、参加者向けの接続情報を表示する。
#   web 系 : コンテナ起動 → Codespaces 転送 URL を表示（Public 化は手動）
#   tcp 系 : コンテナ起動 → ngrok で公開 → 払い出された host:port を表示
# 使い方: export NGROK_AUTHTOKEN=xxxx; bash workshop/up.sh
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")/.."
source workshop/config.sh

NGROK_CONF="$(pwd)/workshop/.ngrok.generated.yml"
NGROK_API="http://127.0.0.1:4040/api/tunnels"
FWD_DOMAIN="${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN:-app.github.dev}"

web_list=(); tcp_list=()

echo "==> コンテナを起動します"
for entry in "${CHALLENGES[@]}"; do
  IFS='|' read -r type name dir port <<< "$entry"
  [ -z "${type:-}" ] && continue
  echo "  - [$type] $name  ($dir, host port $port)"
  if [ ! -f "$dir/docker-compose.yml" ] && [ ! -f "$dir/compose.yml" ]; then
    echo "    !! $dir に compose ファイルが見つかりません。dir を確認してください。" >&2
    continue
  fi
  # PORT を渡す（01-translator は ports: "${PORT:-9999}:9999" を読む。他は無視）
  ( cd "$dir" && COMPOSE_PROJECT_NAME="$name" PORT="$port" docker compose up -d --build )
  if [ "$type" = "web" ]; then web_list+=("$name|$port"); else tcp_list+=("$name|$port"); fi
done

# ---- TCP があれば ngrok 起動 ----
if [ "${#tcp_list[@]}" -gt 0 ]; then
  if [ "${#tcp_list[@]}" -gt 3 ]; then
    echo "!! tcp 問題が ${#tcp_list[@]} 問。ngrok 無料は同時3つまでです。config.sh で絞ってください。" >&2
    exit 1
  fi
  : "${NGROK_AUTHTOKEN:?NGROK_AUTHTOKEN が未設定です。export NGROK_AUTHTOKEN=xxxx を実行してください}"
  echo "==> ngrok 設定を生成"
  {
    echo "version: \"3\""
    echo "agent:"
    echo "  authtoken: ${NGROK_AUTHTOKEN}"
    echo "tunnels:"
    for entry in "${tcp_list[@]}"; do
      IFS='|' read -r name port <<< "$entry"
      echo "  ${name}:"; echo "    proto: tcp"; echo "    addr: ${port}"
    done
  } > "$NGROK_CONF"
  echo "==> ngrok を起動"
  pkill -f "ngrok start" 2>/dev/null || true
  nohup ngrok start --all --config "$NGROK_CONF" >/tmp/ngrok.log 2>&1 &
  for i in $(seq 1 20); do curl -s "$NGROK_API" >/dev/null 2>&1 && break; sleep 1; done
fi

echo ""
echo "============================================================"
echo " 参加者向け 接続情報"
echo "============================================================"
if [ "${#web_list[@]}" -gt 0 ]; then
  echo ""
  echo "[ web 系 ] ブラウザで開く  ※ Ports パネルで該当ポートを Public にすること"
  for entry in "${web_list[@]}"; do
    IFS='|' read -r name port <<< "$entry"
    echo "  - ${name} : https://${CODESPACE_NAME}-${port}.${FWD_DOMAIN}"
  done
fi
if [ "${#tcp_list[@]}" -gt 0 ]; then
  echo ""
  echo "[ tcp 系 ] nc で接続"
  json="$(curl -s "$NGROK_API")"
  for entry in "${tcp_list[@]}"; do
    IFS='|' read -r name port <<< "$entry"
    pub="$(echo "$json" | python3 -c "import sys,json;d=json.load(sys.stdin);print(next((t['public_url'] for t in d['tunnels'] if t['name']=='$name'),''))" 2>/dev/null)"
    if [ -n "$pub" ]; then
      hp="${pub#tcp://}"; host="${hp%%:*}"; rport="${hp##*:}"
      echo "  - ${name} : nc ${host} ${rport}"
    else
      echo "  - ${name} : (取得失敗。 /tmp/ngrok.log を確認)"
    fi
  done
fi
echo "============================================================"
echo "終了するには: bash workshop/down.sh"
