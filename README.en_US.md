# readBCV —— Extract images from article at Bilibili

[![Docker Image](https://img.shields.io/badge/docker%20image-available-green.svg)](https://hub.docker.com/r/boringcat/readbcv/)

## Introduction
readBCV(BCVReader) is a website for extract and create download links for images from article at Bilibili

### Features
- Get raw image link. (Automatic remove `@*.webp` behind normal url)
- Download custom emoticons

### Shortcoming
- Limit speed from server. (Will get 421 if too fast)

### 

### Notes (same as in the page)
Limited by Bilibili. Use **"Download selected links by ......"** is impossible  
~~Or your downloader can create tasks without Referrer in headers~~  
Avoid Bilibili return 421 when access too fast. Each access from server limit at 10 seconds  
The data for each article will keep a week  

## Change logs
### 2020/05/31
- (Fix) Fix a problem that will return video card image when a video inserted in article
- (Fix) Fix a problem cause the frontend generate a bad url when image's "data-src" already have "https"链接的图片了
- (Add) Now we can get the video's cover with had inserted in article
- (Fix) Force backend to return https url. Because browser cannot `fetch` http url under https website

<details>
 <summary>2020/05/27</summary>

- (Fix) Fix a database pool problem with will make backend get data from bilibili multiple times.
- (Fix) Optimize the logic for MetaFile generated

</details>

<details>
 <summary>2020/05/17</summary>

- (Add) Now can show same tag as Bilibili website.
- (Add) Add two button to show and hide pictures.
- (Fix) Fix a problem that may crash the database "can only be used in that same thread.".
- (Fix) Fix a problem that make website hidden "Please Wait".
- (Fix) Fix a problem that website will not show error message from server.

</details>

<details>
 <summary>2020/05/14</summary>

  - Now can get video cover from Bilibili

</details>

<details>
 <summary>2020/05/05</summary>

  - It can deal with cover now
  - Support language "Simplified Chinese", "Traditional Chinese" and "English (United States)"
  - Support "Dark Mode"

</details>

<details>
 <summary>2020/05/04</summary>

  - Add multi architecture support  
    Now supported x86 x86_64 arm32v6 arm32v7 arm64v8 s390x  

    Test with RPI ZW. Database on Synology DS718p docker. I can get about 100ms to 180ms response time in cache mode. And about 1s to 1.4s response time in processing mode

</details>

<details>
 <summary>2020/05/03</summary>

  - Allow input `cv\d+` direct.

</details>

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

## How to add translate?
Run `fontend/gen_i18njs.sh <localeName>`. Then motify `fontend/src/i18n/<locateName>.js` and variable langs in `App.vue`.
**gen_i18njs.sh is depend on grep, tac, head, cut, sed, let. With should be installed by base package in each distribution**

## Deploy
### WARN!
**Maybe some comment in source code is in English. But in most cases. It is in Chinese.**
### Version Variants
- latest: latest version
- _$arch_-%Y-%m-%d: Tag version for _$arch_

### Database Support

|Database|Features|
|:-:|:-|
|SQLite|<li>Memory database only</li><li>Automatic create tables</li><li>rw</li>|
|MySQL/Mariadb|<li>Automatic create tables</li><li>rw</li>|
|Mongo|<li>Automatic create tables</li><li>rw</li>|

### Environment Variables

|Environment|What's Mean|Default|
|:-:|:-:|:-:|
|VIEW|Output log level info| false |
|DEBUG|Output log level debug| false |
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
pushd frontend
yarn install
yarn build
popd
```
#### 3. Copy webpage file to /www
```sh
cp frontend/dist /www/readbcv
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

