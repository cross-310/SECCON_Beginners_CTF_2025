#!/usr/bin/env bash
# =============================================================================
# 出題前のフラグ差し替え（任意・推奨）。
# 対象ディレクトリ配下の flag.txt をダミーに置換する。
#   理由: 元リポジトリには本物のフラグが平文で含まれており、
#         参加者が GitHub を見れば答えが分かってしまうため。
# 注意: 一部の問題はフラグを別の形（ソース埋め込み・環境変数・ビルド引数）で
#       持つ場合があります。各問題の Dockerfile / compose を必ず確認してください。
# 使い方: bash workshop/replace-flags.sh   （up.sh の前に実行）
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")/.."
source workshop/config.sh

for entry in "${CHALLENGES[@]}"; do
  IFS='|' read -r type name dir port <<< "$entry"
  [ -z "${dir:-}" ] && continue
  base="${dir%/build}"   # チャレンジのルート想定
  [ -d "$base" ] || base="$dir"
  while IFS= read -r f; do
    echo "  置換: $f"
    printf '%s\n' "$DUMMY_FLAG" > "$f"
  done < <(find "$base" -type f -name 'flag.txt' 2>/dev/null)
done
echo "==> flag.txt の差し替え完了（見つかったもののみ）。"
