## Readbcv 的 sharevolume 版本帮助

### 0. 版本tag
- boringcat/readbcv:share-YYYY/MM/DD
  日期构建版
- boringcat/readbcv:share
  最新版

### 1. entrypoint操作
0. 在构建时，将前端静态文件拷贝到/opt/readbcv
1. 启动时更新复制 /opt/readbcv 到 /www/readbcv
2. 当用户输入参数时，调用 exec 执行
3. 无参数时，运行 /app/app.pyc

### 2. 使用方法
#### nginx 配置文件示例
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