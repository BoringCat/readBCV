#!/bin/bash

SOURCE=$(command -v source)

[ -z "$SOURCE" ] && echo "You can't use this shell! Please change another one!" && exit 1

cd `dirname $0`

BACKEND='beautifulsoup4 mongoengine'
API='websockets'
LIBS='requests'

create(){
    if [ ! -d .venv ]; then python3 -m virtualenv -p $(command -v python3) .venv; fi
}

update(){
    source .venv/bin/activate
    pip install -U pylint $BACKEND $API $LIBS
    deactivate
}

rm(){
    rm -r .venv
}

COMMAND=$1
[ -z $COMMAND ] && COMMAND='create'

case $COMMAND in
    'create')
        create
        update
    ;;
    'update')
        update
    ;;
    'recreate')
        rm
        create
        update
    ;;
esac
