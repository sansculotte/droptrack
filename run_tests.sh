#!/usr/bin/env bash
if [[ -z "$VIRTUAL_ENV" ]]; then
    source venv/bin/activate
fi

export APP_ENV=config.TestingConfig

py.test "$@"
