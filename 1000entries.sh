#!/bin/bash

ENTRIES=0
if [ -z "$1" ]; then
    TOTAL=1000
else
    TOTAL=$(($1))
fi
PARALLEL=25
IPS=($(./get_neighborlist.sh))
PARALLEL=$((PARALLEL * ${#IPS[*]}))

function add_entry {
    curl -d "entry=$2" -X 'POST' "http://$1/entries" &>/dev/null
    printf "."
}

function run_next {
    if [ $ENTRIES -lt $TOTAL ]; then
        add_entry "${IPS[$ENTRIES % ${#IPS[*]}]}" "t$ENTRIES" &
        ((ENTRIES++))
    fi
}

set -o monitor
trap run_next CHLD

printf "Posting $TOTAL entries"
for i in $(seq 1 $PARALLEL); do
    run_next
done
while [ $ENTRIES -lt $TOTAL ]; do
    wait
done
wait
printf "\nDone\n"
