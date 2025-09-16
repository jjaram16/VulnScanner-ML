#!/usr/bin/env bash
set -euo pipefail
API=${1:-http://127.0.0.1:8090}
curl -fsS "$API/JSON/core/view/version/" | jq .
