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
### 2020/05/01
  - Useable 

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
      DB_HOST: db           # Cache the data to MongoDB. \
      DB_PORT: 27017        # If those environment is empty:\
      DB_USER: readbcv      # DB_HOST、DB_PORT、DB_USER、DB_PASSWD、DB_NAME\
      DB_PASSWD: readbcv    # Program will use SQLite3 memory database automatic
      DB_NAME: readbcv      # The Database Name for program
      DB_AUTHDB: readbcv    # AuthDB for MongoDB user. Default is same as used Database

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
Uncompleted
### Deploy from source code？
Uncompleted
