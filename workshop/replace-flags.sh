#!/usr/bin/env bash
# =============================================================================
# 出題前のフラグ差し替え（推奨）。
#  本リポジトリは問題ごとにフラグの埋め込み方が異なる:
#   - flag.txt 型     : pet_name 等             → 本スクリプトが自動置換
#   - compose env 型  : skipping(FLAG=), 01-translator(FLAG=) → 手動で compose.yml 編集
#   - compose 引数型  : log_viewer(-flag=...)   → 手動で compose.yml 編集
#   - 静的ファイル型  : kingyo_sukui(script.js 等に埋め込み) → 手動で該当ファイル編集
#  → flag.txt は自動、それ以外は WORKSHOP.md の一覧に従って手動で書き換えること。
# 使い方: bash workshop/replace-flags.sh   （up.sh の前に実行）
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")/.."
source workshop/config.sh
for entry in "${CHALLENGES[@]}"; do
  IFS='|' read -r type name dir port <<< "$entry"
  [ -z "${dir:-}" ] && continue
  base="${dir%/build}"; [ -d "$base" ] || base="$dir"
  while IFS= read -r f; do
    echo "  置換: $f"; printf '%s\n' "$DUMMY_FLAG" > "$f"
  done < <(find "$base" -type f -iname 'flag.txt' 2>/dev/null)
done
echo "==> flag.txt の自動置換完了。env/引数/静的埋め込み型は手動対応（WORKSHOP.md 参照）。"
