#!/bin/sh
cd `dirname $0`

_DOCKER_BASENAME='vue'

case $1 in
    '-l')
        [ -z $2 ] && COMMAND=$1 || LISTEN=$2 && COMMNAD=$3
    ;;
    *)
        COMMNAD=$1
        if [ ! -z $2 ] && [ "$2" = "-l" ]; then
            LISTEN=$3
        fi
    ;;
esac
[ -z "$LISTEN" ] && LISTEN="127.0.0.1"


[ -z "$COMMAND" ] && COMMAND="start"

__FRONTEND__=${PWD##*/}
__DIRNAME__=`dirname $PWD`

create() {
    docker create --name=${_DOCKER_BASENAME}_debug_${__FRONTEND__}\
    -v ${__DIRNAME__}:/app\
    -w /app/${__FRONTEND__}\
    -p $LISTEN:3000:3000\
    -e HOST='0.0.0.0' -it boringcat/node_vue:lts-alpine -c "su $UID"
}

start(){
    docker image inspect boringcat/node_vue:lts-alpine > /dev/null 2>/dev/null
    [ $? -ne 0 ] && ./docker-build.sh
    docker container inspect ${_DOCKER_BASENAME}_debug_${__FRONTEND__} > /dev/null 2>/dev/null
    if [ $? -ne 0 ]; then
        create
    else
        OLDLISTEN=$(docker container inspect vue_debug_fontend --format="{{json .HostConfig.PortBindings}}" | jq -r '.[][0].HostIp')
        [ "$OLDLISTEN" != "$LISTEN" ] && rm && create
    fi
    docker start -ia ${_DOCKER_BASENAME}_debug_${__FRONTEND__}
}

rm(){
    docker container rm ${_DOCKER_BASENAME}_debug_${__FRONTEND__}
}

case $COMMAND in
    'start' ) 
        start
    ;;
    'rm' )
        rm
    ;;
    'recreate' )
        rm && start
    ;;
    *)
        echo "Usage: $0 [start|rm|recreate]"
    ;;
esac
