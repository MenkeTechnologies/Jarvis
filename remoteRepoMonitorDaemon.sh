#!/usr/bin/env bash
#{{{ MARK:Header
#**************************************************************
##### Author: JACOBMENKE
##### Date: Thu Apr 12 00:02:45 EDT 2018
##### Purpose: bash script to keep remote hosts in sync with master
##### Notes: watches jarvis dir
#}}}***********************************************************

JARVIS_DIR="$HOME/Jarvis"

[[ ! -d "$JARVIS_DIR" ]] && echo "no $JARVIS_DIR" >&2 && exit 1

gittersmaster() {
    git reset --hard origin/master
    git checkout -B master origin/master
    git pull --force
    git reset --hard origin/master
}

gittersdev() {
    git reset --hard origin/dev
    git checkout -B dev origin/dev
    git pull --force
    git reset --hard origin/dev
}

main() {
    gittersmaster
    pkill webserver.py
    ( python3 webserver.py & >> $JARVIS_DIR/flask.log )
}

while true; do

    cd "$JARVIS_DIR" || {
        echo "$(date) Directory $JARVIS_DIR does not exist" >&2
        exit 1
    }


    echo "starting python3 webserver.py"

    ( python3 webserver.py & >> $JARVIS_DIR/flask.log )
    tail -F "$JARVIS_DIR/flask.log"

    git fetch origin
    output=$(git log HEAD..origin/master --oneline)

    if [[ -n "$output" ]]; then
        echo "$(date) We have change to $(git remote -v)" >&2
        main
    fi

    sleep 10

done
