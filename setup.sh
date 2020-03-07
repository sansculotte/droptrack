#!/usr/bin/env bash

set -e

if [[ $(uname) == 'Linux' ]]; then # go linux
  LIBZMQ=$(dpkg-query -W -f='${Status}' libzmq5-dev 2>/dev/null | grep -c "ok installed")
  if [ $LIBZMQ -eq 0 ]; then
      sudo apt-get install libzmq5-dev
  fi
  VIRTUALENV=$(dpkg-query -W -f='${Status}' python3-virtualenv 2>/dev/null | grep -c "ok installed")
  if [ $VIRTUALENV -eq 0 ]; then
    if [ -x /usr/bin/sudo ]; then
      sudo apt-get install python3 python3-dev python3-pip python-virtualenv
    else
      su -c "apt-get install python3 python3-dev python3-pip virtualenv"
    fi
  fi
elif [[ $(uname) == 'FreeBSD' ]]; then
    pkg install py37-virtualenv libzmq4
else
    echo Unknown System. Dont know what to do.
    exit
fi
# setup virtualenv
virtualenv -p $(which python3.7) venv
venv/bin/pip install -r requirements.txt
