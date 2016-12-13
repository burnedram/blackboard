#!/bin/bash
grep -P '^\s*\d+\.\d+\.\d+\.\d+:\d+\s*$' topologies.txt | sed 's/^ *//;s/ *$//' | sort | uniq -u
