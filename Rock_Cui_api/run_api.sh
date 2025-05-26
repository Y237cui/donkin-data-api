#!/usr/bin/env bash
#!/bin/bash


PORT=8000
PID=$(lsof -ti tcp:$PORT)
if [ -n "$PID" ]; then
  echo "port $PORT occupied $PID , to relseas..."
  kill -9 $PID
fi

echo "open FastAPI ..."
uvicorn get_top:app --reload --port $PORT
# uvicorn get_token_info:app --reload --port $PORT
# 改成需要的 .py
