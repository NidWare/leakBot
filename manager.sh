#!/bin/bash

function build_and_run() {
  docker build -t bot .
  docker run -d --restart unless-stopped --name my_bot bot
}

function stop_and_remove() {
  docker kill my_bot
  docker rm my_bot
}

case $1 in
  start)
    build_and_run
    ;;
  stop)
    stop_and_remove
    ;;
  *)
    echo "Invalid command. Use 'start' to build and run or 'stop' to stop and remove."
    ;;
esac