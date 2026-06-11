#!/usr/bin/env bash
# =============================================================================
# 勉強会で出題するチャレンジ定義（5問構成・確定版）
#   フィールド: type|name|dir|port    （"|" 区切り）
#   type web = Codespaces 転送(ngrok不要) / tcp = ngrok で公開
#   port     = ホスト側公開ポート（各 compose の ports: 左側に一致）
#
#  内訳:
#   web 3問 : kingyo_sukui(33333) / skipping(33455) / log_viewer(9999)
#   tcp 2問 : 01-translator(9001) / pet_name(9080)   ← ngrok 2本（上限3以内）
#
#  注意1: ディレクトリ名は実リポジトリ準拠。01-translator と log_viewer は小文字。
#  注意2: 元 compose では 01-translator も 9999 で log_viewer と衝突するため、
#         01-translator は PORT=9001 に逃がす（up.sh が PORT を渡す。compose 側は
#         ports: "${PORT:-9999}:9999" なので環境変数で上書き可能）。
# =============================================================================

CHALLENGES=(
  "web|kingyo_sukui|misc/kingyo_sukui/build|33333"
  "web|skipping|web/skipping/build|33455"
  "web|log_viewer|web/log_viewer/build|9999"
  "tcp|01-translator|crypto/01-translator/build|9001"
  "tcp|pet_name|pwnable/pet_name/build|9080"
)

DUMMY_FLAG='ctf4b{workshop_dummy_flag_replace_me}'
