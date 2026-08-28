#!/usr/bin/env bash
set -euo pipefail

# Generic human-action scaffold. Customize stages; never hard-code secrets.

TOTAL_STAGES=0
CURRENT_STAGE=0

stage() {
  CURRENT_STAGE=$((CURRENT_STAGE + 1))
  printf '\n[%d/%d] %s\n' "$CURRENT_STAGE" "$TOTAL_STAGES" "$1"
}

say() { printf '%s\n' "$*"; }

confirm() {
  local prompt=${1:-Continue?}
  local answer
  read -r -p "$prompt [y/N] " answer
  [[ "$answer" =~ ^[Yy]$ ]]
}

ask() {
  local prompt=$1
  local value
  read -r -p "$prompt: " value
  printf '%s' "$value"
}

ask_secret() {
  local prompt=$1
  local value
  read -r -s -p "$prompt: " value
  printf '\n' >&2
  printf '%s' "$value"
}

# Example:
# TOTAL_STAGES=1
# stage "Configure the private dashboard"
# say "Open the exact project page and create the required value."
# token=$(ask_secret "Token (kept only in memory)")
# confirm "The dashboard reports success?" || exit 1
# unset token

say "Customize this script with the precise human-only stages before running it."
