#!/bin/bash
make_neighborlist() {
    grep -P '^\s*\d+\.\d+\.\d+\.\d+:\d+\s*$' topologies.txt | sed 's/^ *//;s/ *$//' | sort | uniq -u
}

add_entry() {
    entryid=($(curl -d "entry=$2&return_id=1" -X 'POST' "http://$1/entries" 2>/dev/null))
    entryid=${entryid[0]}
    (
        flock -x 200
        if [ ! -z "$3" ]; then
            printf "$3"
        fi
        . /dev/shm/ENTRIES
        ENTRIES+=($entryid)
        declare -p ENTRIES > /dev/shm/ENTRIES
    ) 200>$LOCK
}

ENTRIES=()
declare -p ENTRIES > /dev/shm/ENTRIES
START_ENTRIES=5
FLOOD_ENTRIES=20
LOCK=$(mktemp)

START=0
printf "Adding $START_ENTRIES entries"
while [ $START -lt $START_ENTRIES ]; do
    for ipport in $(make_neighborlist); do
        if [ $START -ge $START_ENTRIES ]; then
            break
        fi
        add_entry "$ipport" "t$START" "." &
        ((START++))
    done
done
wait
printf "\n"
echo -n "Press enter when the board has reached consistency"
read user

printf "Posting $FLOOD_ENTRIES requests"
FLOOD=0
while [ $FLOOD -lt $FLOOD_ENTRIES ]; do
    for ipport in $(make_neighborlist); do
        if [ $FLOOD -ge $FLOOD_ENTRIES ]; then
            break
        fi
        . /dev/shm/ENTRIES
        entryid=${ENTRIES[$RANDOM % ${#ENTRIES[@]}]}
        post=""
        rnd=$((RANDOM % 5))
        if [ $rnd -lt 2 ]; then
            printf "+"
            add_entry "$ipport" "f$((START + FLOOD))" &
        else
            if [ $rnd -lt 4 ] ; then
                printf "/"
                post="entry=m${#ENTRIES[@]}&id=$entryid&delete=0"
            elif [ $rnd -eq 4 ]; then
                printf "-"
                post="entry=d${#ENTRIES[@]}&id=$entryid&delete=1"
            fi
            curl -d "$post" -X 'POST' "http://${ipport}/entries" 2>/dev/null 1>&2 &
        fi
        ((FLOOD++))
        #sleep .5
    done
done
printf "\n"

echo "Waiting for requests to finish..."
wait
rm $LOCK
rm /dev/shm/ENTRIES
echo "Done"
