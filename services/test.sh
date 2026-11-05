#!/bin/bash
# Start both services, curl every endpoint, print results, then stop them.
cd "$(dirname "$0")"
./start-all.sh
sleep 1
echo ""
echo "== dealers :3001 =="
for url in health dealers dealers/1 dealers/2/models inventory makes dealers/99; do
  echo "--- GET /$url"
  curl -s -w "\n[HTTP %{http_code}]\n" "http://127.0.0.1:3001/$url"
done
echo ""
echo "== reviews :3002 =="
for url in health reviews "reviews?dealerId=1" "reviews?dealerId=2" "reviews/dealer/3"; do
  echo "--- GET /$url"
  curl -s -w "\n[HTTP %{http_code}]\n" "http://127.0.0.1:3002/$url"
done
echo "--- POST /reviews"
curl -s -w "\n[HTTP %{http_code}]\n" -X POST -H "Content-Type: application/json" \
  -d '{"dealer_id":1,"name":"Test","purchase":false,"car_make":"Ford","car_model":"F-150","car_year":2023,"sentiment":"positive","review":"Test review."}' \
  http://127.0.0.1:3002/reviews
echo "--- GET /reviews?dealerId=1 (after POST, in-memory only)"
curl -s "http://127.0.0.1:3002/reviews?dealerId=1" | head -c 600; echo ""
./stop-all.sh
