#!/bin/sh

cp -ur /opt/readbcv /www/readbcv

[ ! -z "$*" ] && exec "$@"

cd /app

exec /usr/bin/env python app.pyc
