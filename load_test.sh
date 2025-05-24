#!/bin/bash

# magic that will kill our children when the script exits
trap "kill 0" EXIT

HOST=$1
PORT=$2
CLIENTS=$3

for client in `seq 1 $CLIENTS`
do
  echo Client_$client is sending messages as fast as possible
  python3 test_client.py Client_$client $HOST $PORT &
done

wait

echo done