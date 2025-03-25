#!/bin/bash

PORT="${PORT:-8080}"
CORS_ALLOW_ORIGIN="http://localhost:5173;http://localhost:8080"

export CORS_ALLOW_ORIGIN="$CORS_ALLOW_ORIGIN"
uvicorn open_webui.main:app --port $PORT --host 0.0.0.0 --forwarded-allow-ips '*' --reload