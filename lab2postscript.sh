#!/bin/bash
ENTRY=1
DELETE=5
printf "Adding some entries"
while [ $ENTRY -le $DELETE ]; do
    while [ $ENTRY -le $DELETE ] && read ipport; do
        post="entry=t${ENTRY}"
        ((ENTRY++))
        curl -d "$post" -X 'POST' "http://${ipport}/entries" 2>/dev/null 1>&2
        printf "."
    done <neighborlist.txt
done
printf "\n"
for i in `seq 1 3`; do
    printf "Posting round ${i}"
    while read ipport; do
        post=""
        rnd=$((RANDOM % 5))
        if [ $ENTRY -le $DELETE ] || [ $rnd -lt 2 ]; then
            post="entry=t${ENTRY}"
            ((ENTRY++))
        elif [ $rnd -lt 4 ] ; then
            post="entry=m${DELETE}&id=${DELETE}&delete=0"
            ((DELETE++))
        elif [ $rnd -eq 4 ]; then
            post="entry=d${DELETE}&id=${DELETE}&delete=1"
            ((DELETE++))
        fi
        curl -d "$post" -X 'POST' "http://${ipport}/entries" 2>/dev/null 1>&2 &
        printf "."
    done <neighborlist.txt
    printf "\n"
done
echo "Waiting for requests to finish..."
wait
echo "Done"
