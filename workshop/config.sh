#!/usr/bin/env bash
# =============================================================================
# 勉強会で出題するチャレンジの定義ファイル
# -----------------------------------------------------------------------------
# 1行 = 1チャレンジ。フィールドは "|" 区切りで以下の4つ。
#
#   type   : web  … HTTP/HTTPS。Codespaces のポート転送で公開（ngrok 不要）
#            tcp  … 生TCP（pwnable / nc 接続型 crypto・misc）。ngrok で公開
#   name   : 表示名（ngrok のトンネル名にも使う。英数字とアンダースコアのみ）
#   dir    : docker-compose.yml があるディレクトリ（リポジトリ相対）
#   port   : そのチャレンジの compose の ports: 左側（ホスト側ポート）と一致させる
#
# 重要:
#   - tcp タイプは最大3問まで（ngrok 無料の同時エンドポイント上限）
#   - port は各チャレンジの build/docker-compose.yml を開いて
#     "ports: - \"9080:9000\"" の左側（9080）を必ず確認して書くこと
# =============================================================================

CHALLENGES=(
  # --- web 系（ngrok を消費しない。何問でも可）---
  "web|login4b|web/login4b/build|3000"
  # "web|memo4b|web/memo4b/build|8080"
  # "web|skipping|web/skipping/build|8081"

  # --- tcp 系（ngrok 無料は合計3問まで）---
  "tcp|pet_name|pwnable/pet_name/build|9080"
  # "tcp|pet_sound|pwnable/pet_sound/build|9081"
  # "tcp|pivot4b|pwnable/pivot4b/build|9082"
)

# ダミーフラグ（勉強会用に flag.txt を差し替える場合に使用）
DUMMY_FLAG='ctf4b{workshop_dummy_flag_replace_me}'
