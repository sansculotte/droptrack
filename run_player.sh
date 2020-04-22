#!/bin/sh
set -e

#if [ -n "$1" ]; then
#    ssh -f -o ExitOnForwardFailure=yes -N -T -M -L 80:localhost:80 -L 5200:localhost:5200 "$1"
#fi

python3 -m player "$@"
