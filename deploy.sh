#!/bin/bash

echo "🚀 Building and deploying Meet bots..."

# Build Docker image
docker build -t meet-bots .

# Run with your meeting URL
docker run -d \
  --name nepali-bots \
  -e MEET_URL=https://meet.google.com/oru-azsu-cmo \
  meet-bots

echo "✅ 50 Nepali bots deployed!"
echo "📊 Check logs: docker logs nepali-bots"
echo "🛑 Stop bots: docker stop nepali-bots"