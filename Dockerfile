# Create base image first. Beacuse frontend change more frequently then backend
FROM python:3.7-alpine as python_nginx_base
ARG apkmirror=mirrors.sjtug.sjtu.edu.cn
ARG pipmirror=https://pypi.tuna.tsinghua.edu.cn/simple

# Setup base config
WORKDIR /app
ENV APP_LISTEN='127.0.0.1'\
    APP_PORT='8765'\
    APP_PATH='/api/v1/readcv'

VOLUME [ "/var/log" ]
ENTRYPOINT [ "/docker-entrypoint.sh" ]

# ------------------------------------------ #
# Copy python depend config and install then
COPY backend/envsetting.sh /
RUN set -xe\
 && sed -i "s/dl-cdn.alpinelinux.org/${apkmirror}/g" /etc/apk/repositories\
 && apk add --update --no-cache gcc musl-dev nginx\
 && pip config set global.index-url ${pipmirror}\
 && source /envsetting.sh\
 && pip install --no-cache-dir -U supervisor $BACKEND $API $LIBS\
 && apk del gcc musl-dev\
 && mkdir -p /var/log/nginx /run/nginx\
 && rm /etc/nginx/conf.d/default.conf\
 && sed -i '/error_log/s!/.*log!/dev/stderr!g;/access_log/s!/.*log!/dev/stdout!g' /etc/nginx/nginx.conf

# Build the frontend
FROM node:lts-alpine as WebBuilder
ARG apkmirror=mirrors.sjtug.sjtu.edu.cn
ARG npmmirror=https://registry.npm.taobao.org
# Install git for `yarn install`
RUN set -xe\
 && mkdir /app\
 && cd /app\
 && sed -i "s/dl-cdn.alpinelinux.org/${apkmirror}/g" /etc/apk/repositories\
 && apk add --no-cache git\
 && yarn config set registry "${npmmirror}"
COPY fontend /app
RUN set -xe\
 && cd /app\
 && yarn install\
 && yarn build\
 && mv /app/dist /tmp/dist\
 && cd /\
 && rm -r /app

# Use the base image and copy all directory in it.
FROM python_nginx_base
COPY --from=WebBuilder --chown=nginx:nginx /tmp/dist /www/BCVReader
COPY backend /app
COPY root /
RUN set -xe\
 && python -m compileall .\
 && for n in $(find -name "*.pyc"); do mv $n $(echo $n | sed 's/__pycache__\///g' | awk -F '.' '{$(NF-1)="";for(i=1;i<=NF;i++){if($i!=""){printf"."$i}};print""}');done\
 && cp -v libs/*.pyc /usr/local/lib/python*/\
 && find -type f ! -name "*.pyc" -a | xargs rm -v\
 && find -type d ! -name "db" -a ! -name "." | xargs rm -vr || true\
 && chmod +x /docker-entrypoint.sh
