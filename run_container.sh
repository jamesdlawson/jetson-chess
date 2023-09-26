#!/bin/zsh

docker build -t jetson-chess-image:latest --label jestson-chess-label -f Dockerfile  .

echo Delete old container...
docker rm -f jetson-chess

echo Pruning old image...
docker image prune --force --filter='label=jestson-chess-label'

echo Run new container...
docker run -dit --name jetson-chess jetson-chess-image:latest
