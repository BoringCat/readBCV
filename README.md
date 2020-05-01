# readBCV —— 提取B站专栏图片

[![Docker Image](https://img.shields.io/badge/docker%20image-available-green.svg)](https://hub.docker.com/r/boringcat/readbcv/)

## 介绍
readBCV(BCVReader) 是一个用于分析获取B站专栏图片的页面

### 用途
- 批量下载原图(自动分析去除 `@*.webp` )
- 获取表情包

### 缺陷
- 服务器限流（怕被B站421）
- 无法获取封面（它是onload生成的）

### 注意事项（与页面中相同）
由于B站限制，无法直接实现右键菜单 **“使用......下载选定链接”**  
~~你的下载器可以不带Referrer就当我没说~~  
为防止B站返回421，后端处理速度限制为10秒/个  
服务器缓存数据时间为7天  

## 更新版本
### 2020/05/01
  - 初步完成

## 使用方法
0. 在B站看到好康的图片或表情包的专栏（CV）
1. 复制URL地址（电脑），分享—>复制链接（手机客户端）
2. 进入页面，粘贴地址
3. 点击分析
4. 复制批量链接到下载器，或点击链接（图片）下载文件，也可以右键图片另存为 ~~（反正显示图片又不用我服务器的流量）~~


## 部署
### 版本号说明
- latest：最新版本
- build-%Y-%m-%d：Tag版本

### docker-compose（推荐）
``` yaml
version: '2'
services:
  readbcv:
    image: boringcat/readbcv:latest
    restart: on-failure
    links:
      - readbcv_db:db
    environment:
      DB_HOST: db           # Mongo数据库设定，用于持久化缓存 \
      DB_PORT: 27017        # 若不设定 DB_HOST、DB_PORT、DB_USER \
      DB_USER: readbcv      # DB_PASSWD、DB_NAME 将自动使用SQLite3 \
      DB_PASSWD: readbcv    # 内存数据库
      DB_NAME: readbcv      # 数据库表名
      DB_AUTHDB: readbcv    # 账号认证用数据库，默认为 $DB_NAME

  readbcv_db:               # Mongo数据库，具体设置参考 https://hub.docker.com/_/mongo
    image: mongo:4
    restart: on-failure
    volumes: 
      - /srv/datas/mongo:/data/db
      - /etc/localtime:/etc/localtime:ro
    environment: 
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: root
      TZ: Asia/Shanghai

```

### docker？
未完成（咕咕咕）
### 源码部署？
未完成（咕咕咕）
