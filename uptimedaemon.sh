#!/usr/bin/env bash

# declare some variables for later
google_success=false
cloudflare_success=false
timeout=30 #timeout after 30 seconds
sleeptime=10

# constantly loop for all time
while true; do

    # ping google and check if a response is recieved
    if ping -c 1 -t $timeout 8.8.8.8 &>/dev/null; then
        google_success=true
    else
        google_success=false
    fi

    # ping cloudflare and check if a response is recieved
    if ping -c 1 -t $timeout 1.1.1.1 &>/dev/null; then
        cloudflare_success=true
    else
        cloudflare_success=false
    fi

    if [[ "$cloudflare_success" = false ]] && [[ "$google_success" = false ]]; then
        echo "Both pings timed out -- internet down?"
    fi

    sleep $sleeptime
done
