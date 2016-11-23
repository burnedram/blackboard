#!/bin/bash
echo "<html><body>"
for y in `cat neighborlist.txt` 
do 
echo "<iframe src=\"http://$y\" width="31%" height=450></iframe>"
done
echo "</body></html>"
