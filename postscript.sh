#!/bin/bash
ENTRY=1
for i in `seq 1 3`; do
    printf "Posting round ${i}"
    while read ipport; do
        curl -d "entry=t${ENTRY}" -X 'POST' "http://${ipport}/entries" 2>/dev/null 1>&2
        printf "."
        ((ENTRY++))
    done <neighborlist.txt
    printf "\n"
done

