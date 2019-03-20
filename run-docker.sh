#!/bin/bash
GENDATA=${GENDATA:-true}

if $GENDATA; then
    # Run with sample data
    echo "Generating sample data and launching httplogmon"
    /usr/local/bin/python3 /usr/src/tests/gen-sample-data.py > /var/log/access.log && /usr/local/bin/python3 /usr/src/httplogmon/main.py
else
    echo "Creating log file and running httplogmon"
    touch /var/log/access.log && /usr/local/bin/python3 /usr/src/httplogmon/main.py
fi
