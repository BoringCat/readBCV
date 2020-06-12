## Help and example for version sharevolume

### 0. tags
- boringcat/readbcv:share-YYYY/MM/DD
  version build in YYYY/MM/DD
- boringcat/readbcv:share
  latest version

### 1. Diff for entrypoints
0. We will copy html files to /opt/readbcv instead /www/readbcv
1. When you run/start this image/container. We will upgrade files in /www/readbcv from /opt/readbcv
2. If no command from user. We will run /app/app/pyc

### 2. How to use
#### Examlpe for nginx config file
```
server {
    listen 80;
    server_name readbcv;

    location /api {
        proxy_pass_request_headers  on;
        proxy_http_version          1.1;
        proxy_set_header            Upgrade $http_upgrade;
        proxy_set_header            Connection "Upgrade";
        proxy_set_header            Host $host;
        proxy_pass                  http://readbcv:8765;
    }
    location / {
        root    /www/readbcv;
        index   index.html;
    }
}
```
In config. the `readbcv` in `http://readbcv:8765` is alias name for readbcv's container  
`root    /www/readbcv;` is a folder where the html files are.

#### Docker-cli
``` sh
docker run --name=readbcv --restart=unless-stopped\
    -v /path/to/save/html:/www/readbcv\
    -l some_db_or_not:db\
    -e DB_TYPE=$Which_DB_you_choose\
    -e DB_PORT=$DB_IP_or_hostname_if_not_sqlite\
    -e DB_USER=$DB_login_user_if_not_sqlite\
    -e DB_PASSWD=$DB_login_password_if_not_sqlite\
    -e DB_NAME=$Name_for_database_if_not_sqlite\
    -e DB_AUTHDB=$DB_auth_db_for_mongo\
    -d boringcat/readbcv:share

docker run --name=nginx --restart=unless-stopped\
    -l readbcv:readbcv
    -v /path/to/save/html:/www/readbcv:ro\
    -v /path/to/your/configs:/etc/nginx/conf.d:ro\
    -p 80:80\
    -p 443:443\
    -d nginx:$which_you_like
```
All environments in readbcv is same as [README.md](../README.en_US.md)

#### docker-compose
``` yaml
version: '2'
services:
  readbcv:
    image: boringcat/readbcv:share
    restart: unless-stopped
    volumes:
      - readbcv_web:/www/readbcv

  web:
    image: nginx
    restart: unless-stopped
    ports:
      - 80:80
      - 443:443
    volumes:
      - readbcv_web:/www/readbcv:ro
      - /path/to/your/configs:/etc/nginx/conf.d:ro

volumes:
  readbcv_web:

```
Same as Docker-cli but use docker volume instead host folder.