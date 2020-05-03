# readBCV —— Extract images from article at Bilibili

[![Docker Image](https://img.shields.io/badge/docker%20image-available-green.svg)](https://hub.docker.com/r/boringcat/readbcv/)

## Introduction
readBCV(BCVReader) is a website for extract and create download links for images from article at Bilibili

### Features
- Get raw image link. (Automatic remove `@*.webp` behind normal url)
- Download custom emoticons

### Shortcoming
- Limit speed from server. (Will get 421 if too fast)
- Unable to get Cover. (It generated at `window.onload`)

### 

### Notes (same as in the page)
Limited by Bilibili. Use **"Download selected links by ......"** is impossible  
~~Or your downloader can create tasks without Referrer in headers~~  
Avoid Bilibili return 421 when access too fast. Each access from server limit at 10 seconds  
The data for each article will keep a week  

## Change logs
### 2020/05/03
  - Allow input `cv\d+` direct.
<details>
 <summary>2020/05/02</summary>

  - Add support for MySQL/Mariadb
  - Complete README.md

</details>

<details>
 <summary>2020/05/01</summary>

- Useable

</details>

## Guide
0. When you read some wonderful pictures in article at Bilibili
1. Copy article's URL (For website). "Share"->"Copy Link" (For phone app)
2. Open the website, paste the url in inputbox
3. Check the button.
4. Now you get link for each picture in article. Enjoy!

## Deploy
### WARN!
**Maybe some comment in source code is in English. But in most cases. It is in Chinese.**
### Version variants
- `latest`: The latest build (Same as latest build-*)
- build-%Y-%m-%d: Version for each tag.

### Database Support

|Database|Features|
|:-:|:-|
|SQLite|<li>Memory database only</li><li>Automatic create tables</li><li>rw</li>|
|MySQL/Mariadb|<li>Automatic create tables</li><li>rw</li>|
|Mongo|<li>Automatic create tables</li><li>rw</li>|

### Version Variants
- latest: latest version
- build-%Y-%m-%d: Tag version

### Environment Variables

|Environment|What's Mean|Default|
|:-:|:-:|:-:|
|DB_TYPE|Type of database| SQLite |
|DB_HOST|Address of database| - |
|DB_PORT|Port of database| - |
|DB_USER|Username of database| - |
|DB_PASSWD|Password of database| - |
|DB_NAME|Database name to use| - |
|DB_AUTHDB|Auth database for MongoDB|Same as DB_NAME|

### Use docker-compose (recommend)
``` yaml
version: '2'
services:
  readbcv:
    image: boringcat/readbcv:latest
    restart: on-failure
    links:
      - readbcv_db:db
    environment:
      DB_TYPE: Mongo
      DB_HOST: db
      DB_PORT: 27017
      DB_USER: readbcv
      DB_PASSWD: readbcv
      DB_NAME: readbcv
      DB_AUTHDB: readbcv

  readbcv_db:               # MongoDB，For specific settings, please refer to https://hub.docker.com/_/mongo
    image: mongo:4
    restart: on-failure
    volumes: 
      - /srv/datas/mongo:/data/db
      - /etc/localtime:/etc/localtime:ro
    environment: 
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: root
      TZ: Asia/Shanghai     # Your area

```

### Use docker？
#### 0. Build Image (Pull is better)
``` sh
$ pwd
/path/to/project
$ docker build -t <Repository>:<Tag> .
```
#### 1. Create database container (Ignore if you already have database)
```sh
docker run --name readbcv_db --restart on-failure \
    -v /srv/datas/mongo:/data/db \
    -v /etc/localtime:/etc/localtime:ro \
    -e MONGO_INITDB_ROOT_USERNAME=root \
    -e MONGO_INITDB_ROOT_PASSWORD=root \
    -e TZ=Asia/Shanghai \
    -d mongo:4
```
#### 2. Config database's account, privileges
Custom step......
#### 3. Create App container
```sh
docker run --name readbcv --restart on-failure \
    --link readbcv_db:db \
    -e DB_TYPE=Mongo \
    -e DB_HOST=db \
    -e DB_PORT=27017 \
    -e DB_USER=readbcv \
    -e DB_PASSWD=readbcv \
    -e DB_NAME=readbcv \
    -e DB_AUTHDB=readbcv \
    -p 8080:80 \
    -d boringcat/readbcv:latest
```

### Deploy from source code (no recommend)
#### 1. Get source code
```sh
git clone --depth 1 https://github.com/BoringCat/readBCV.git
cd readBCV
```
#### 2. Build web page
```sh
pushd fontend
yarn install
yarn build
popd
```
#### 3. Copy webpage file to /www
```sh
cp fontend/dist /www/readbcv
chown -R <wwwuser>:<wwwgroup> /www/readbcv
```
#### 4. Config and start/reload web server
Custom step......
#### 5. Create virtualenv for backend
```sh
pushd backend
./setupenv.sh
```
#### 6. Start backend
```sh
# (In other terminal or tmux/screen or in systemd or anything else)
source /path/to/readbcv/backend/.venv/bin/activate
python app.py
```

