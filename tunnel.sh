#/bin/sh
SERVER=$1
ssh -f -N -T -M -L 5200:localhost:5200 -L 5210:localhost:5210 $SERVER
