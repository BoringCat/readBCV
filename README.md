# readBCV —— 提取B站专栏图片

[![Docker Image](https://img.shields.io/badge/docker%20image-available-green.svg)](https://hub.docker.com/r/boringcat/readbcv/)

[English Version](README.en_US.md)

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
### 2020/05/02
  - 添加 MySQL/Mariadb 数据库支持
  - 完善 README
<details>
 <summary>2020/05/01</summary>

- 初步完成

</details>

## 使用方法
0. 在B站看到好康的图片或表情包的专栏（CV）
1. 复制URL地址（电脑），分享—>复制链接（手机客户端）
2. 进入页面，粘贴地址
3. 点击分析
4. 复制批量链接到下载器，或点击链接（图片）下载文件，也可以右键图片另存为 ~~（反正显示图片又不用我服务器的流量）~~


## 部署
### 数据库支持

|数据库|支持度|
|:-:|:-|
|SQLite|<li>仅内存数据库</li><li>自动创建表</li><li>读写</li>|
|MySQL/Mariadb|<li>自动创建表</li><li>读写</li>|
|Mongo|<li>自动创建表</li><li>读写</li>|

### 版本号说明
- latest：最新版本
- build-%Y-%m-%d：Tag版本

### 环境变量说明

|环境变量|用途|默认情况|
|:-:|:-:|:-:|
|DB_TYPE|数据库类型| SQLite |
|DB_HOST|数据库地址| - |
|DB_PORT|数据库端口| - |
|DB_USER|连接数据库的用户名| - |
|DB_PASSWD|连接数据库的密码| - |
|DB_NAME|数据库的库名| - |
|DB_AUTHDB|Mongo数据库的认证库名|与DB_NAME相同|

### docker-compose（推荐）
``` yaml
version: '2'
services:
  readbcv:
    image: boringcat/readbcv:latest
    restart: on-failure
    ports:
      - 8080:80
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

### docker
#### 0. Build 镜像
``` sh
$ pwd
/path/to/project
$ docker build -t <Repository>:<Tag> .
```
#### 1. 创建数据库容器（已有数据库可忽略）
```sh
docker run --name readbcv_db --restart on-failure \
    -v /srv/datas/mongo:/data/db \
    -v /etc/localtime:/etc/localtime:ro \
    -e MONGO_INITDB_ROOT_USERNAME=root \
    -e MONGO_INITDB_ROOT_PASSWORD=root \
    -e TZ=Asia/Shanghai \
    -d mongo:4
```
#### 2. 配置数据库权限，新建数据库
略
#### 3. 创建容器
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

### 源码部署（不推荐）
#### 1. 获取源码
```sh
git clone --depth 1 https://github.com/BoringCat/readBCV.git
cd readBCV
```
#### 2. 构建前端
```sh
pushd fontend
yarn install
yarn build
popd
```
#### 3. 拷贝前端文件到/www
```sh
cp fontend/dist /www/readbcv
chown -R <wwwuser>:<wwwgroup> /www/readbcv
```
#### 4. 配置、启动/重载Web服务器
略
#### 5. 创建后端virtualenv
```sh
pushd backend
./setupenv.sh
```
#### 6. 启动后端
```sh
# (其他终端 或 tmux/screen 或 systemd 或 .....)
source /path/to/readbcv/backend/.venv/bin/activate
python app.py
```
