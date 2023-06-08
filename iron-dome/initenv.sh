#!/bin/bash
set -e
ENVFILE=/usr/src/environment
[[ -n $EXTMON ]] && echo "EXTMON=\"$EXTMON\"" >> /usr/src/environment || true
[[ -n $DIRMON ]] && echo "DIRMON=\"$DIRMON\"" >> /usr/src/environment || true