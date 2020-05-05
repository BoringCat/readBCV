#!/bin/bash

SOURCE=$(command -v source)

[ -z "$SOURCE" ] && echo "You can't use this shell! Please change another one!" && exit 1

cd `dirname $0`

source ./envsetting.sh

PY3_VERSION=$(python3 -V | cut -d' ' -f2| cut -d. -f1-2 | sed 's/\.//g')

create(){
    if [ ! -d "$AIM" ]; then python3 -m virtualenv -p $(command -v python3) --no-download $AIM; fi
}

update(){
    source $AIM/bin/activate
    pip install -U pip wheel setuptools pylint $BACKEND $API $LIBS
    [ $PY3_VERSION -gt 37 ] && venvlib=$(realpath .venv/lib/python3.*/site-packages) || venvlib=$(realpath .venv/lib/python3.*)
    for py in libs/*.py
    do
    ln -rvsf $py ${venvlib}/
    done
    deactivate
}

del(){
    rm -r $AIM
}

COMMAND=$1
AIM=$2
[ -z $COMMAND ] && COMMAND='create'
[ -z $AIM ] && AIM='.venv'

case $COMMAND in
    'create')
        create
        update
    ;;
    'update')
        update
    ;;
    'recreate')
        del
        create
        update
    ;;
esac
