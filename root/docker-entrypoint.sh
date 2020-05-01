#!/bin/sh

[ ! -z "$*" ] && exec "$@"

exec /usr/local/bin/supervisord -n -c /etc/supervisord.conf
