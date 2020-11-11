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
[MetaFile Help](docs/MetaFileHelp.en_US.md)

## Change logs
### 2020/11/11
- (Add) Add custom TTL for cache. default is 7 days.

### 2020/06/12
- (Fix) Fix a problem which is cause by nginx.conf changed
- (Add) New version: sharevolume. This version build without nginx but have static html files. You need to mount /www/readbcv in container into web server.  
  [Need more help?](docs/ShareVolume.en_US.md)
- (Add) Now support Redis!
  - Support signal point unencryption connect; select database(maybe)
  - Used datatype: String
  - Key: $id
- (Add) Sqlite database now support use db file (By default still memory database)
  - How to use: `env DB_NAME=/path/to/dbfile`  
    **Warning: DB_TYPE MUST BE "sqlite" or none of environment value will be used**

<details>
 <summary>2020/06/07</summary>

- (Add) New feature: Get image list for Photo album @ bilibili  
  - For users: You can just paste the url from `https://h.bilibili.com/`. Or input "h" + $ID
  - For Database: It's id is "h" + $ID
- (Motify) Change the way for connected database. Now each thread will get it's own link.  
  - (Unknown) For SQLite memory database. Some time the backend will retuen "UnKnown Error" and terminal show error `no such table: cvcache`. It is caused by multiple threads. I can not reappear the problem.  
    _(It maybe fine for other databases)__
  **WARNING: For SQLite database. This change will cause large memory use. Because each Thread queue will get it own database**
- (Motify) The "Download With MetaLink" button will be hide if there is only one image
- (Motify) May add sort url support. ( Or may not :( )

</details>

<details>
 <summary>2020/06/06</summary>

- (Fix) Now return human readable error message when page not found.
- (Add) Add a python script to compose metafiles. (In Chinese)

</details>

<details>
 <summary>2020/05/31</summary>

- (Fix) Fix a problem that will return video card image when a video inserted in article
- (Fix) Fix a problem cause the frontend generate a bad url when image's "data-src" already have "https"链接的图片了
- (Add) Now we can get the video's cover with had inserted in article
- (Fix) Force backend to return https url. Because browser cannot `fetch` http url under https website
- (Fix) Now the figcaption support `<br>`

</details>

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
|KEY_TTL|TTL for cache| 7(days) |

### Use docker-compose (recommend)
``` yaml
version: '2'
services:
  readbcv:
    image: boringcat/readbcv:latest
    restart: on-failure
    links:
      - readbcv_redis:rds
    environment:
      DB_TYPE: redis
      DB_HOST: rds
      KEY_TTL: 7

  readbcv_redis:               # Redis，For specific settings, please refer to https://hub.docker.com/_/redis
    image: redis:alpine        # Recommend alpine 
    restart: on-failure
    volumes:
      - /etc/localtime:/etc/localtime:ro
    environment: 
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
docker run --name readbcv_redis --restart on-failure \
    -v /etc/localtime:/etc/localtime:ro \
    -e TZ=Asia/Shanghai \
    -d redis:alpine
```
#### 2. Create App container
```sh
docker run --name readbcv --restart on-failure \
    --link readbcv_redis:rds \
    -e DB_TYPE=redis \
    -e DB_HOST=rds \
    -e KEY_TTL=7 \
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

