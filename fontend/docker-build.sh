#!/bin/sh
cd `dirname $0`

U_ID=`id -u $USERNAME`
G_ID=`id -g $USERNAME`

if [ $U_ID -eq 1000 ]; then
    CMD="sed -i 's/^node:x:1000/1000:x:1000/g' /etc/passwd"
else
    CMD="echo \"$U_ID:x:$U_ID:$G_ID::/home/$U_ID:/bin/sh\" >> /etc/passwd"
fi

if [ $G_ID -eq 1000 ]; then
    CMD=$CMD" && sed -i 's/^node:x:1000/1000:x:1000/g' /etc/group"
else
    CMD=$CMD" && echo \"$G_ID:x:$G_ID:$G_ID\" >> /etc/group"
fi

CMD=$CMD" && \
sed -i 's/dl-cdn.alpinelinux.org/mirrors.sjtug.sjtu.edu.cn/g' /etc/apk/repositories && \
apk add --no-cache --update git && \
yarn global add @vue/cli"

docker image rm boringcat/node_vue:lts-alpine
docker run --entrypoint=/bin/sh --name=vue-com -v $PWD:/app  -w /app -it node:lts-alpine -c "$CMD"
docker container commit vue-com boringcat/node_vue:lts-alpine
docker container rm vue-com
