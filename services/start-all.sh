#!/bin/bash
# Start both back-end services in the background (dealers :3001, reviews :3002).
# Runs `node server.js` directly so the recorded PIDs are the servers themselves.
cd "$(dirname "$0")"
ROOT="$PWD"
( cd "$ROOT/dealers-service" && exec node server.js > "$ROOT/dealers.log" 2>&1 & echo $! > "$ROOT/dealers.pid" )
( cd "$ROOT/reviews-service" && exec node server.js > "$ROOT/reviews.log" 2>&1 & echo $! > "$ROOT/reviews.pid" )
sleep 2
echo "dealers service:  http://127.0.0.1:3001/health (pid $(cat "$ROOT/dealers.pid"))"
echo "reviews service:  http://127.0.0.1:3002/health (pid $(cat "$ROOT/reviews.pid"))"
