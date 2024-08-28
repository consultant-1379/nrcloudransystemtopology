#!/bin/bash
#
# Build and start the wiremock container for use in the test
#
docker stop $(docker ps -a -q) || true
docker rm $(docker ps -a -q) || true
docker image prune
docker-compose -f docker-compose.yml down --rmi all --remove-orphans
docker-compose -f docker-compose.yml build --force-rm
docker-compose -f docker-compose.yml up --build -d