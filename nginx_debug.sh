#!/bin/sh

cd `dirname $0`

docker run\
    -v $PWD/readbcv.local.conf:/etc/nginx/conf.d/readbcv.conf:ro\
    --network=host\
    --name="nginx-debug"\
    --rm -it nginx:alpine nginx -g "daemon off;"
