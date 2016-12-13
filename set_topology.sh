#!/bin/bash

if [ -z "$1" ]; then
    echo "usage: ./set_topology.sh <topology>"
    exit
fi

for ipport in $(./get_neighborlist.sh); do
    curl -d "set_topology=$1" -X 'POST' "http://${ipport}/entries" 2>/dev/null 1>&2 &
done
