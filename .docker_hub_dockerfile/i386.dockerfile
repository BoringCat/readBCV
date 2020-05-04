FROM debian:10-slim as qemu_downloader
RUN set -xe\
 && apt-get update\
 && apt-get install --no-install-recommends qemu-user-static

FROM node:lts-alpine as WebBuilder

COPY fontend /app
WORKDIR /app
RUN set -xe\
 && cd /app\
 && apk add --no-cache git\
 && yarn install\
 && yarn build\
 && mv /app/dist /tmp/dist\
 && cd /\
 && rm -r /app

FROM i386/python:3.7-alpine

COPY --from=qemu_downloader /usr/bin/qemu-i386-static /usr/bin/
COPY backend /app
WORKDIR /app

RUN set -xe\
 && apk add --update --no-cache gcc musl-dev net-snmp-dev nginx\
 && cd /app/\
 && source ./envsetting.sh\
 && pip install --no-cache-dir -U supervisor $BACKEND $API $LIBS\
 && apk del gcc musl-dev net-snmp-dev\
 && mkdir -p /var/log /run/nginx

COPY --from=WebBuilder --chown=nginx:nginx /tmp/dist /www/BCVReader
COPY root /
RUN set -xe\
 && rm /etc/nginx/conf.d/default.conf\
 && python -m compileall .\
 && for n in $(find -name "*.pyc"); do mv $n $(echo $n | sed 's/__pycache__\///g' | awk -F '.' '{$(NF-1)="";for(i=1;i<=NF;i++){if($i!=""){printf"."$i}};print""}');done\
 && cp -v libs/*.pyc /usr/local/lib/python*/\
 && find -type f ! -name "*.pyc" -a | xargs rm -v\
 && find -type d ! -name "db" -a ! -name "." | xargs rm -vr || true\
 && chmod +x /docker-entrypoint.sh

ENV APP_LISTEN='127.0.0.1'\
    APP_PORT='8765'\
    APP_PATH='/api/v1/readcv'

VOLUME [ "/var/log" ]
ENTRYPOINT [ "/docker-entrypoint.sh" ]
