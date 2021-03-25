#!/bin/sh

set -eux

docker build -t gpu_scraper .

if docker stop -t 1 gpu_scraper; then
  echo "Container was running"

  docker rm gpu_scraper
fi

docker run -d -e TELEGRAM_TOKEN -e TELEGRAM_CHAT_ID --name=gpu_scraper --restart=unless-stopped gpu_scraper