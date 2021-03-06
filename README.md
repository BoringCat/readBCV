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

### 注意事项（与页面中相同）
由于B站限制，无法直接实现右键菜单 **“使用......下载选定链接”**  
~~你的下载器可以不带Referrer就当我没说~~  
为防止B站返回421，后端处理速度限制为10秒/个  
服务器缓存数据时间为7天  
[MetaFile Help](docs/MetaFileHelp.md)

## 更新版本
### 2020/11/12
- (Fix) 修复解析BV时URL错误的问题
- (Fix) 修复手机端获取的问题
  注意：手机端出于B站限制，无法获取到cv封面
- (Add) 增加URL跳转支持
  例：手机访问cvXXXXXXXX会自动跳转到mobile/XXXXXXXX。源逻辑判断为获取失败，现在能正常返回数据了

### 2020/11/11
- (Add) 增加自定义过期时间（天）
- (Motify) 修改Redis的使用方式

<details>
 <summary>2020/06/12</summary>

- (Fix) 修复因Nginx默认配置更新导致无法启动的错误
- (Add) 增加一个不带 nginx 的版本，需要手动挂载容器内的 /www/readbcv 到 web 服务器中  
  更多帮助 [Example of share volume](docs/ShareVolume.md)
- (Add) 现在支持使用 Redis 数据库了
  - 支持度： 正常无加密连接单节点，切换数据库(? 未验证)
  - 存储的数据类型: String
  - 键: $id
- (Add) Sqlite 数据库现在支持使用文件（默认仍然是内存）
  - 传递方法： 环境变量 DB_NAME  
    **警告：必须设置DB_TYPE，否则任何 DB_ 开头的设置都不会生效**

</details>

<details>
 <summary>2020/06/07</summary>

- (Add) 增加分析相簿图片的功能（最多也就9个，我怎么就怎么懒呢？）  
  - 对于用户：粘贴相簿的 URL 或 在ID前加h 即可进行分析
  - 对于数据库：继续使用源 cvcache 表，相簿前缀为h
- (Motify) 修改数据库使用方式，每个分析线程独立一个链接  
  - (Unknown) SQLite数据库可能会出现无法复现的错误 `no such table: cvcache`， 系多线程操作造成，未定位到具体操作与代码逻辑  
    _（其他实体数据库不会出现问题(大概)）_
  **警告：对于SQLite内存数据库来说，这将增加大量的内存使用**
- (Motify) 现在“使用MetaLink下载”按钮会在只有一张图片时隐藏
- (Motify) 可能会加入短链接支持 （ 也可能不会 :( ）

</details>

<details>
 <summary>2020/06/06</summary>

- (Fix) 修复找不到专栏页面时无法返回错误信息的问题
- (Add) 增加一个组合metafile文件的脚本

</details>

<details>
 <summary>2020/05/31</summary>

- (Fix) 修复当专栏中插入视频时返回辣个图片的问题
- (Fix) 修复图片自带https前缀时获取失败的问题，现在可以匹配任意链接的图片了
- (Add) 现在可以匹配专栏中插入视频的封面了
- (Fix) 强制后端返回https链接，以应对https下无法`fetch` http图片的问题
- (Fix) 现在标签支持换行了

</details>

<details>
 <summary>2020/05/27</summary>

- (Fix) 修复可能会出现的数据库连接问题导致重复获取数据的问题
- (Fix) 优化MetaFile下载方式逻辑

</details>

<details>
 <summary>2020/05/17</summary>

- (Add) 现在可以显示跟B站一样的Tag了
- (Add) 增加“展开”和“折叠”按钮
- (Fix) 修复了数据库可能会出现的多线程访问出错
- (Fix) 修复WEB端不会出现等待提示的问题
- (Fix) 修复WEB端不会报出服务器返回错误的问题

</details>

<details>
 <summary>2020/05/05</summary>

  - 现在可以获取视频封面了

</details>

<details>
 <summary>2020/05/05</summary>

  - 现在可以获取封面了
  - 支持三种语言： "简体中文"、"繁体中文"、"英语（美国）"
  - 支持暗色主题

</details>

<details>
 <summary>2020/05/04</summary>

- 增加多架构支持，现在支持x86 x86_64 arm32v6 arm32v7 arm64v8 s390x。  
  
  在树莓派ZW上测试，数据库在NAS的情况下，缓存模式跑出了100毫秒到180毫秒的成绩，实时获取数据也能在1秒到1.4秒内返回  
  (启动10分钟，测试一瞬间)

</details>

<details>
 <summary>2020/05/03</summary>

  - 允许直接输入 `cv\d+`

</details>

<details>
 <summary>2020/05/02</summary>

- 添加 MySQL/Mariadb 数据库支持
- 完善 README

</details>

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

## 增添翻译方法
运行 `fontend/gen_i18njs.sh <localeName>`，然后修改 `fontend/src/i18n/<locateName>.js` 和 App.vue 中的 langs 变量即可
**gen_i18njs.sh 依赖于 grep, tac, head, cut, sed, let. 这些命令应该内置与shell中或在每个发行版中最小化安装时安装**

## 部署
### 版本号说明
- latest：最新版本
- _$arch_-%Y-%m-%d：_$arch_ 架构的Tag版本

### 数据库支持

|数据库|支持度|
|:-:|:-|
|SQLite|<li>仅内存数据库</li><li>自动创建表</li><li>读写</li>|
|MySQL/Mariadb|<li>自动创建表</li><li>读写</li>|
|Mongo|<li>自动创建表</li><li>读写</li>|

### 环境变量说明

|环境变量|用途|默认情况|
|:-:|:-:|:-:|
|VIEW|详细输出模式| false |
|DEBUG|调试模式| false |
|DB_TYPE|数据库类型| SQLite |
|DB_HOST|数据库地址| - |
|DB_PORT|数据库端口| - |
|DB_USER|连接数据库的用户名| - |
|DB_PASSWD|连接数据库的密码| - |
|DB_NAME|数据库的库名| - |
|DB_AUTHDB|Mongo数据库的认证库名|与DB_NAME相同|
|KEY_TTL|缓存过期时间（天）| 7 |

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
      - readbcv_redis:rds
    environment:
      DB_TYPE: redis
      DB_HOST: rds
      KEY_TTL: 7

  readbcv_redis:               # Mongo数据库，具体设置参考 https://hub.docker.com/_/mongo
    image: redis:alpine        # 推荐alpine
    restart: on-failure
    volumes: 
      - /etc/localtime:/etc/localtime:ro
    environment: 
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
docker run --name readbcv_redis --restart on-failure \
    -v /etc/localtime:/etc/localtime:ro \
    -e TZ=Asia/Shanghai \
    -d redis:alpine
```
#### 2. 创建容器
```sh
docker run --name readbcv --restart on-failure \
    --link readbcv_redis:rds \
    -e DB_TYPE=redis \
    -e DB_HOST=rds \
    -e KEY_TTL=7 \
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
