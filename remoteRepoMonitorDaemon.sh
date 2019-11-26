#!/usr/bin/env bash
#{{{ MARK:Header
#**************************************************************
##### Author: JACOBMENKE
##### Date: Thu Apr 12 00:02:45 EDT 2018
##### Purpose: bash script to keep remote hosts in sync with master
##### Notes: watches jarvis dir
#}}}***********************************************************

JARVIS_DIR="$HOME/Jarvis"

if [[ -f $HOME/IP.sh ]];then
  source $HOME/IP.sh
  echo "IP is $IP"
else
  echo "no IP.sh"
fi


trap 'kill $pid1 $pid2;exit 1' INT QUIT

export IP=$IP
echo "global ip is $IP"


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

killa() {
    echo "killing gunicorn webserver.py"
    pkill -f gunicorn && echo killed gunicorn
    gunicorn --threads 5 --workers 1 --bind 0.0.0.0:3000 webserver:app
    echo "killing python3 sockets.py"
    pkill -f sockets.py && echo killed sockets
    echo "starting webserver.py in background"
    python3 webserver.py &
    pid1=$!
    echo "starting sockets.py in background"
    python3 sockets.py &
    pid2=$!
}

main() {
    gittersmaster
    killa
}

cd "$JARVIS_DIR" || {
    echo "$(date) Directory $JARVIS_DIR does not exist" >&2
    exit 1
}

killa

while true; do

    cd "$JARVIS_DIR" || {
        echo "$(date) Directory $JARVIS_DIR does not exist" >&2
        exit 1
    }

    #tail -F "$JARVIS_DIR/flask.log"

    git fetch origin
    output=$(git log HEAD..origin/master --oneline)

    if [[ -n "$output" ]]; then
        echo "$(date) We have change to $(git remote -v)" >&2
        main
    fi

    sleep 10

done
