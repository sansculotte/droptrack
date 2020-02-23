#!/usr/bin/env bash

if [ -z "$VIRTUAL_ENV" ]; then
    source venv/bin/activate
fi

export FLASK_ENV=Development
export FLASK_APP=$(pwd)/webapp
export FLASK_DEBUG=1
flask run
